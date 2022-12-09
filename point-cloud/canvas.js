const canvas = document.getElementById("main");
const context = canvas.getContext("2d");

const w = 1200;
const h = 800;
const labelPadding = 0.5;

d3.select(canvas).attr("width", w).attr("height", h).style("background-color", "#222");

d3.csv("glove_connections_2.csv").then(links => {
    d3.json("precomp-nodes.json").then(nodes => {
        console.log(links, nodes);

        const linksProcessed = links.map((d, i) => {
            return {
                x1: nodes.find(x => x.index === +d.course_index_1)?.x || 0,
                y1: nodes.find(x => x.index === +d.course_index_1)?.y || 0,
                x2: nodes.find(x => x.index === +d.course_index_2)?.x || 0,
                y2: nodes.find(x => x.index === +d.course_index_2)?.y || 0,
                source: +d.course_index_1,
                target: +d.course_index_2,
                strength: +d.similarity,
            }
        });

        console.log(linksProcessed);

        d3.select(canvas).call(d3.zoom()
            .translateExtent([[-10 * w, -10 * h], [10 * w, 10 * h]])
            .scaleExtent([0.1, 10])
            .on("zoom", ({transform}) => zoomed(transform)));

        function zoomed(transform) {
            const r = Math.min(1.5, 5 / transform.k);

            context.save();
            context.clearRect(0, 0, w, h);
            context.translate(transform.x, transform.y);
            context.scale(transform.k, transform.k);
            context.beginPath();
            context.lineWidth = 0.5 / transform.k;
            for (const {x1, y1, x2, y2, strength} of linksProcessed) {
                context.strokeStyle = `rgba(255,0,0,${Math.max(0, 0.5 * ((strength - 0.8) * 5))})`;
                context.moveTo(x1, y1);
                context.lineTo(x2, y2);
            }
            context.stroke();
            context.fillStyle = "red";
            context.beginPath();
            for (const {x, y} of nodes) {
                context.moveTo(x + r, y);
                context.arc(x, y, r, 0, 2 * Math.PI);
            }
            context.fill();

            context.font = `${12 / transform.k}px "IBM Plex Mono", monospace`;

            const letterWidth = context.measureText("t").width;
            const letterHeight = context.measureText("T").fontBoundingBoxAscent + context.measureText("T").fontBoundingBoxDescent;

            let labeledNodes = [];

            for (let i in nodes) {
                const thisNode = nodes[i];
                const thisCourseTitle = thisNode.title;
                const titleWidth = thisCourseTitle.length * letterWidth;
                const thisLeft = thisNode.x - titleWidth / 2;
                const thisRight = thisNode.x + titleWidth / 2;
                const thisTop = thisNode.y - r;
                const thisBottom = thisNode.y + letterHeight - r;

                if (labeledNodes.every(d => {
                    const dLeft = d.x - d.title.length * letterWidth / 2;
                    const dRight = d.x + d.title.length * letterWidth / 2;
                    const dTop = d.y - r - labelPadding * letterHeight;
                    const dBottom = d.y + letterHeight - r + labelPadding * letterHeight;
                    const isFree = dLeft > thisRight || dRight < thisLeft || dTop > thisBottom || dBottom < thisTop;
                    return isFree;
                })) {
                    context.fillStyle = "rgba(255,0,0,0.5)";
                    context.fillRect(thisNode.x - titleWidth / 2, thisNode.y - r - letterHeight, titleWidth, letterHeight);
                    context.fillStyle = "rgba(255,255,255,0.5)";
                    context.fillText(thisCourseTitle, thisNode.x - titleWidth / 2, thisNode.y - r);

                    labeledNodes.push(thisNode);
                }
            }

            context.restore();
        }

        canvas.onmousemove = e => {
            const r = canvas.getBoundingClientRect();
            const x = e.clientX - r.left;
            const y = e.clientY - r.top;


        }

        zoomed(d3.zoomIdentity);
    });
});