import {randomBytes} from "crypto";

function getCounter() {
    return Math.floor(Math.random() * (0xFFFFFF + 1));
}

class ObjectID{
    private static pid = process.pid;
    private static randPart = randomBytes(5);
    private inc = getCounter();

    private getProcessRandom() {
        const pid = process.pid;
        if(pid != ObjectID.pid) {
            ObjectID.pid = pid;
            ObjectID.randPart = randomBytes(5);
        }
        return ObjectID.randPart;
    }

    constructor() {
        const timestamp = Math.floor(Date.now() / 1000).toString(16);
        const random = this.getProcessRandom().toString("hex");
        const counter = this.inc.toString(16);
        const objectId = `${timestamp}${random}${counter}`;


    }

}