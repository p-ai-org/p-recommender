const svg = d3.select("svg");

const w = 1200;
const h = 800;

svg
    .attr("width", w)
    .attr("height", h);

d3.csv("courses_temp.csv").then(courses => {
    d3.csv("links_temp.csv").then(links => {
        const linksProcessed = links.map(d => ({
            source: courses.findIndex(x => x.id === d.id1),
            target: courses.findIndex(x => x.id === d.id2),
            strength: d.strength,
        }));

        const force = d3.forceSimulation(courses)
            .force("charge", d3.forceManyBody().strength(-200))
            .force("link", d3.forceLink(linksProcessed).strength(d => d.strength))
            .force("center", d3.forceCenter(w/2, h/2))
            .force("collision", d3.forceCollide().radius(10))
            .on("tick", tick);

        function tick() {
            const nodes = svg.selectAll("circle.course")
                .data(courses)
                .join("circle")
                .attr("class", "course")
                .attr("r", 10)
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("fill", "red");

            const links = svg.selectAll("line.link")
                .data(linksProcessed)
                .join("line")
                .attr("class", "link")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y)
                .attr("stroke", "red")
                .attr("stroke-width", d => Math.sqrt(d.strength) * 4)
                // .style("opacity", d => d.strength);
        }
    });
})