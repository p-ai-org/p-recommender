const svg = d3.select("svg");

const w = 1200;
const h = 800;

svg
    .attr("width", w)
    .attr("height", h)
    .attr("viewbox", [0, 0, w, h]);

const bg = svg.append("rect").attr("width", w).attr("height", h).attr("fill", "white");

d3.json("alex_courses.json").then(courses => {
    d3.csv("alex_connections.csv").then(links => {
        const g = svg.append("g");

        const coursesProcessed = Object.keys(courses.title).map(d => ({
            id: courses.identifier[d],
            title: courses.title[d],
            description: courses.description[d],
        }));

        const linksProcessed = links.map(d => ({
            source: +d.node1,
            target: +d.node2,
            strength: +d.score,
        })).sort((a, b) => b.strength - a.strength).splice(0, 10000);

        const simulation = d3.forceSimulation(coursesProcessed)
            .force("charge", d3.forceManyBody().strength(-100))
            .force("link", d3.forceLink(linksProcessed).strength(d => d.strength))
            .force("center", d3.forceCenter(w/2, h/2))
            // .force("collision", d3.forceCollide().radius(5))
            .stop();

        const loading = g.append("text").text("loading...");

        d3.timeout(() => {
            for (let i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
                simulation.tick();
            }

            loading.remove();

            const links = g.selectAll("line.link")
                .data(linksProcessed)
                .join("line")
                .attr("class", "link")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y)
                .attr("stroke", "red")
                // .attr("stroke-width", d => Math.sqrt(d.strength) * 4)
                .attr("stroke-width", 2)
                .style("opacity", d => d.strength);

            const nodes = g.selectAll("circle.course")
                .data(coursesProcessed)
                .join("circle")
                .attr("class", "course")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", d => 3)
                .attr("fill", d => "red")
                .on("click", (e, d) => {
                    updateGraph(d.id);
                });

            const text = g.selectAll("text.courseLabel")
                .data(coursesProcessed)
                .join("text")
                .attr("text-anchor", "middle")
                .attr("class", "courseLabel")
                .attr("x", d => d.x)
                .attr("y", d => d.y)
                .text(d => d.title)
                .attr("font-size", "6px")
                .style("opacity", "0.75")
                .attr("fill", "red");

            bg.on("click", updateGraph());

            function updateGraph(highlightId) {
                links
                    .style("opacity", d => (!highlightId || d.source.id === highlightId || d.target.id === highlightId) ? d.strength : d.strength * 0.1);

                nodes
                    .attr("r", d => d.id === highlightId ? 10 : 3)
                    .attr("fill", d => d.id === highlightId ? "blue" : "red")
                    .style("opacity", d => (!highlightId || d.id === highlightId || linksProcessed.filter(x => x.target.id === highlightId || x.source.id === highlightId).map(x => (x.target.id === highlightId) ? x.source.id : x.target.id).includes(d.id)) ? 1 : 0.1);

                text
                    .style("opacity", d => (!highlightId || d.id === highlightId || linksProcessed.filter(x => x.target.id === highlightId || x.source.id === highlightId).map(x => (x.target.id === highlightId) ? x.source.id : x.target.id).includes(d.id)) ? 1 : 0.1);
            }
        });

        svg.call(d3.zoom()
            .translateExtent([[-10 * w, -10 * h], [10 * w, 10 * h]])
            .scaleExtent([0.1, 10])
            .on("zoom", zoomed)
        );

        function zoomed({transform}) {
            g.attr("transform", transform);
        }
    });
})