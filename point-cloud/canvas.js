const canvas = document.getElementById("main");
const context = canvas.getContext("2d");

const w = 1200;
const h = 800;
const labelPadding = 0.5;

d3.select(canvas).attr("width", w).attr("height", h).style("background-color", "#222");

d3.csv("glove_connections_2.csv").then(links => {
    d3.json("precomp-nodes.json").then(nodes => {
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

        d3.select(canvas).call(d3.zoom()
            .translateExtent([[-10 * w, -10 * h], [10 * w, 10 * h]])
            .scaleExtent([0.1, 10])
            .on("zoom", ({transform}) => update(transform, lastSelectedIndex)));

        let lastTransform = d3.zoomIdentity;
        let lastSelectedIndex = null;

        function update(transform, selectedIndex) {
            const r = Math.min(1.5, 5 / transform.k);
            const linkedIndices = [...new Set(linksProcessed.filter(d => [d.source, d.target].includes(selectedIndex)).reduce((a, b) => [...a, b.source, b.target], []))];
            let labeledNodes = [];

            context.save();
            context.clearRect(0, 0, w, h);
            context.translate(transform.x, transform.y);
            context.scale(transform.k, transform.k);
            context.beginPath();
            context.lineWidth = 0.5 / transform.k;

            context.strokeStyle = `rgba(255,0,0,0.3)`;

            for (const {x1, y1, x2, y2} of linksProcessed.filter(d => !linkedIndices.includes(d.source) && !linkedIndices.includes(d.target))) {
                context.moveTo(x1, y1);
                context.lineTo(x2, y2);
            }

            context.stroke();
            context.beginPath();

            if (linkedIndices.length) {
                context.strokeStyle = "blue";
                for (const {x1, y1, x2, y2} of linksProcessed.filter(d => [d.target, d.source].includes(selectedIndex))) {
                    context.moveTo(x1, y1);
                    context.lineTo(x2, y2);
                }

                context.stroke();
                context.beginPath();
            }

            if (linkedIndices.length) {{
                const selectedNode = nodes.find(d => d.index === selectedIndex);
                const selectedRadius = 10;
                context.fillStyle = "blue";
                context.moveTo(selectedNode.x + selectedRadius, selectedNode.y);
                context.arc(selectedNode.x, selectedNode.y, selectedRadius, 0, 2 * Math.PI);
                context.fill();

                context.beginPath();

                for (const {x, y} of nodes.filter(d => linkedIndices.includes(d.index) && d.index !== selectedIndex)) {
                    context.fillStyle = "red";
                    context.moveTo(x + r, y);
                    context.arc(x, y, r, 0, 2 * Math.PI);
                }
                context.fill();

                context.beginPath();

                for (const {x, y} of nodes.filter(d => !linkedIndices.includes(d.index))) {
                    context.fillStyle = "rgba(255,0,0,0.1)";
                    context.moveTo(x + r, y);
                    context.arc(x, y, r, 0, 2 * Math.PI);
                }
                context.fill();
            }} else {
                for (const {x, y} of nodes) {
                    context.fillStyle = "red";
                    context.moveTo(x + r, y);
                    context.arc(x, y, r, 0, 2 * Math.PI);
                }
                context.fill();
            }

            context.font = `${12 / transform.k}px "IBM Plex Mono", monospace`;

            const letterWidth = context.measureText("t").width;
            const letterHeight = context.measureText("T").fontBoundingBoxAscent + context.measureText("T").fontBoundingBoxDescent;


            for (let i of (linkedIndices.length ? linkedIndices : nodes)) {
                const thisNode = linkedIndices.length ? nodes[i] : i;
                const thisCourseTitle = thisNode.title;
                const titleWidth = thisCourseTitle.length * letterWidth;
                const thisLeft = thisNode.x - titleWidth / 2;
                const thisTop = thisNode.y - r;
                const thisRight = thisNode.x + titleWidth / 2;
                const thisBottom = thisNode.y + letterHeight - r;

                if (linkedIndices.length ? linkedIndices : labeledNodes.every(d => {
                    const dLeft = d.x - d.title.length * letterWidth / 2;
                    const dRight = d.x + d.title.length * letterWidth / 2;
                    const dTop = d.y - r - labelPadding * letterHeight;
                    const dBottom = d.y + letterHeight - r + labelPadding * letterHeight;
                    const isFree = dLeft > thisRight || dRight < thisLeft || dTop > thisBottom || dBottom < thisTop;
                    return isFree;
                })) {
                    context.fillStyle = (thisNode.index === selectedIndex) ? "rgba(0,0,255,0.5)" : "rgba(255,0,0,0.5)";
                    context.fillRect(thisLeft, thisTop - letterHeight, titleWidth, letterHeight);
                    context.fillStyle = "rgba(255,255,255,0.5)";
                    context.fillText(thisCourseTitle, thisLeft, thisTop);

                    if (!linkedIndices.length) labeledNodes.push(thisNode);
                }
            }

            context.restore();

            lastTransform = transform;
        }

        canvas.onmousemove = e => {
            const r = canvas.getBoundingClientRect();
            const x = e.clientX - r.left;
            const y = e.clientY - r.top;
        }

        update(lastTransform, lastSelectedIndex);

        const courseInput = document.getElementById("courseSearch");
        const courseButton = document.getElementById("courseSearchButton");
        const clearButton = document.getElementById("clearButton");

        clearButton.onclick = () => {
            update(lastTransform, null);
            lastSelectedIndex = null;
        }

        courseButton.onclick = () => {
            const inputValue = courseInput.value;
            const thisCourse = nodes.find(d => d.id === inputValue);
            if (!thisCourse) return alert("no course found for this id");
            update(lastTransform, thisCourse.index);
            lastSelectedIndex = thisCourse.index;
        }
    });
});