import cluster from "cluster";
import ObjectID from "./objectid.only.number";
const numCPUs = require('os').cpus().length;

// test unique

console.log("테스트 유니크")
const start = Date.now();
const arrayIds = new Array<string>();
const setIds = new Set<string>();
while (Date.now() - start < 1000) {
    const id = new ObjectID().toString();
    arrayIds.push(id);
    setIds.add(id);
}
console.log(arrayIds.length);
console.log(arrayIds.length === setIds.size);

// test multiprocessing
console.log("테스트 멀티프로세싱");
const arrayIds2 = new Array<string>();
const setIds2 = new Set<string>();
const Pool = require('multiprocessing').Pool;

function job() {
    const id = new ObjectID().toString();
    arrayIds2.push(id);
    setIds2.add(id);
}

const pool = new Pool(numCPUs);
pool.map(job).catch((err: any) => {});
console.log(arrayIds2.length === setIds2.size);
process.exit(1);