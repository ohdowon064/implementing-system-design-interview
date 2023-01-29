import {randomBytes} from "crypto";
import Mutex from "./mutex";
import cluster from "cluster";
const numCPUs = require('os').cpus().length;


function getCounter() {
    return Math.floor(Math.random() * (0xFFFFFF + 1));
}

class ObjectID {
    private readonly id: string;
    private static pid = process.pid;
    private static rand = randomBytes(5);
    private static inc = getCounter();
    private static mutex = new Mutex();

    private getProcessRandom(): Buffer {
        const pid = process.pid;
        if (pid != ObjectID.pid) {
            ObjectID.pid = pid;
            ObjectID.rand = randomBytes(5);
        }
        return ObjectID.rand;
    }

    private static increment(): void {
        ObjectID.inc = (ObjectID.inc + 1) % (0xFFFFFF + 1);
    }

    private getTimestampPart(): number {
        return Math.floor(Date.now() / 1000)
    }

    private getRandomPart(): number {
        return parseInt(this.getProcessRandom().toString("hex"), 16)
    }

    private getCounterPart(): number {
        return ObjectID.inc;
    }

    constructor() {
        const timestamp = this.getTimestampPart();
        const random = this.getRandomPart();
        const counter = this.getCounterPart();

        this.id = `${timestamp}${random}${counter}`;
        ObjectID.increment();
    }


    public toString(): string {
        return this.id;
    }
}

// test unique
console.log("테스트 유니크")
const start = Date.now();
const arrayIds = new Array<string>();
const setIds = new Set<string>();
while (Date.now() - start < 100) {
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

if (cluster.isMaster) {
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
} else {
    const id = new ObjectID().toString();
    arrayIds2.push(id);
    setIds2.add(id);
}

console.log(arrayIds2.length === setIds2.size);

export default ObjectID;