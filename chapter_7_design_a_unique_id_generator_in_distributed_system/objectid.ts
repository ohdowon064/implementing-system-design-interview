import {randomBytes} from "crypto";
import AsyncLock = require("async-lock");

function getCounter() {
    return Math.floor(Math.random() * (0xFFFFFF + 1));
}

class ObjectID{
    private id: string;
    private static pid = process.pid;
    private static rand = randomBytes(5);
    private static inc = getCounter();
    private static lock = new AsyncLock();

    private getProcessRandom(): Buffer {
        const pid = process.pid;
        if(pid != ObjectID.pid) {
            ObjectID.pid = pid;
            ObjectID.rand = randomBytes(5);
        }
        return ObjectID.rand;
    }

    private static increment(): void {
        ObjectID.inc = (ObjectID.inc + 1) % (0xFFFFFF + 1);
    }

    private getTimestampPart(): string {
        return Math.floor(Date.now() / 1000).toString(16);
    }

    private getRandomPart(): string {
        return this.getProcessRandom().toString("hex");
    }

    private getCounterPart(): string {
        return ObjectID.inc.toString(16);
    }

    constructor() {
        const timestamp = this.getTimestampPart();
        const random = this.getRandomPart();

        let objectId = `${timestamp}${random}`;

        ObjectID.lock.acquire("inc", (done) => {
            objectId += this.getCounterPart();
            ObjectID.increment();
        });

        this.id = objectId;
    }

}