const svg = d3.select("svg");

const w = 1200;
const h = 800;

svg
    .attr("width", w)
    .attr("height", h)
    .attr("viewbox", [0, 0, w, h]);

const bg = svg.append("rect").attr("width", w).attr("height", h).attr("fill", "white");

d3.json("precomp-nodes-fixed-indices.json").then(courses => {
    d3.csv("glove_connections_2.csv").then(links => {
        const g = svg.append("g");

        const coursesProcessed = courses.map(d => ({
            id: d.id,
            title: d.title,
            index: d.index,
            // description: d.description,
        })).sort((a, b) => +a.index - +b.index);

        console.log(coursesProcessed[0]);

        const linksProcessed = links.map((d, i) => {
            // console.log(d.course_index_1);
            return {
                source: +d.course_index_1,
                target: +d.course_index_2,
                strength: Math.max(0, (+d.similarity - 0.4)) * 1.67,
                // defaultShow: Math.random() > 0.8
                // strength: +d.similarity,
            }
        });

        const simulation = d3.forceSimulation(coursesProcessed)
            .force("charge", d3.forceManyBody().strength(-100))
            .force("link", d3.forceLink(linksProcessed).strength(d => d.strength))
            .force("center", d3.forceCenter(w/2, h/2))
            .stop();

        let isLoading = false;

        for (let i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
            simulation.tick();
        }

        console.log(linksProcessed, coursesProcessed);

        const linkNodes = g.selectAll("line.link")
            .data(linksProcessed) // .filter(() => Math.random() > 0.8)
            .join("line")
            .attr("class", "link")
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y)
            .attr("stroke", "red")
            // .attr("stroke-width", d => Math.sqrt(d.strength) * 4)
            .attr("stroke-width", 2)
            .style("opacity", d => 0.2 * d.strength);

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
            .attr("font-size", "24px")
            .style("opacity", "0.75")
            .attr("fill", "black");

        function updateGraph(highlightId) {
            linkNodes
                .style("opacity", d => (!highlightId || d.source.id === highlightId || d.target.id === highlightId) ? d.strength : d.strength * 0.1);

            nodes
                .attr("r", d => d.id === highlightId ? 10 : 3)
                .attr("fill", d => d.id === highlightId ? "blue" : "red")
                .style("opacity", d => (!highlightId || d.id === highlightId || linksProcessed.filter(x => x.target.id === highlightId || x.source.id === highlightId).map(x => (x.target.id === highlightId) ? x.source.id : x.target.id).includes(d.id)) ? 1 : 0.1);

            text
                .style("opacity", d => (!highlightId || d.id === highlightId || linksProcessed.filter(x => x.target.id === highlightId || x.source.id === highlightId).map(x => (x.target.id === highlightId) ? x.source.id : x.target.id).includes(d.id)) ? 1 : 0);
        }

        updateGraph();

        const thisField = d3.select("input#courseSearch");
        const thisButton = d3.select("button#courseSearchButton");

        thisButton.on("click", () => {
            const thisId = thisField._groups[0][0].value;
            if (coursesProcessed.some(d => d.id === thisId)) {
                updateGraph(thisId);
            } else {
                console.log("invalid id");
            }
        });

        svg.call(d3.zoom()
            .translateExtent([[-10 * w, -10 * h], [10 * w, 10 * h]])
            .scaleExtent([0.1, 10])
            .on("zoom", zoomed)
        );

        function zoomed({transform}) {
            if (!isLoading) {
                isLoading = true;

                g.attr("transform", transform);

                isLoading = false;
            }
        }
    });
})