const connections = require("./precomp-nodes.json");
const indices = require("./indexed_course_ids.json");
const fs = require("fs");

const newConnections = connections.map(course => {
    let newCourse = {...course};
    newCourse.index = Object.values(indices).findIndex(d => d === newCourse.id);
    return newCourse;
});

const thisJson = JSON.stringify(newConnections);

fs.writeFile("precomp-nodes-fixed-indices.json", thisJson, "utf8", () => console.log("done writing"));