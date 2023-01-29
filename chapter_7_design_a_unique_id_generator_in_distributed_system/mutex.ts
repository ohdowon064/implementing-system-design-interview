const awaitUnlock = async (mutex: Mutex) => {
    if(!mutex.isLocked()) {
        return Promise.resolve();
    }
    return new Promise<void>((resolve) => {
        setTimeout(() => {
            awaitUnlock(mutex).then(() => resolve())
        }, 100)
    })
}

export default class Mutex {
    private locked: boolean;
    constructor() {
        this.locked = false;
    }

    public isLocked(): boolean {
        return this.locked;
    }

    async lock() {
        await awaitUnlock(this);
        this.locked = true;
    }

    release() {
        this.locked = false;
    }
}

