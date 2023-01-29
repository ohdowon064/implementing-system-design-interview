import {randomBytes} from "crypto";
import Mutex from "./mutex";


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

export default ObjectID;