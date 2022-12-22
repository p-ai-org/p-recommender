const connections = require("./precomp-nodes.json");
const indices = require("./indexed_course_ids.json");
const fs = require("fs");

let notFoundCounter = 0;

const newConnections = connections.map(course => {
    let newCourse = {...course};
    const newId = newCourse.id.toUpperCase();
    let newIndex = Object.values(indices).findIndex(d => d === newId);
    if (newIndex === -1) {
        newIndex = Object.values(indices).length + notFoundCounter;
        console.log(newIndex);
        notFoundCounter++;
    }
    newCourse.id = newId;
    newCourse.index = newIndex;
    return newCourse;
});

const thisJson = JSON.stringify(newConnections);

fs.writeFile("precomp-nodes-fixed-indices.json", thisJson, "utf8", () => console.log("done writing"));