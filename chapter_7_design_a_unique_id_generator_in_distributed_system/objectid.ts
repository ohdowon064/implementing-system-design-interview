import {randomBytes} from "crypto";

function getCounter() {
    return Math.floor(Math.random() * (0xFFFFFF + 1));
}

class ObjectID{
    private pid = process.pid;
    private randPart = randomBytes(5);
    private inc = getCounter();

    constructor() {

    }

}