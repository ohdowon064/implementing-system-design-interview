import ObjectID from "./objectid.only.number";

function onlyUnique(value: any, index: any, self: any) {
    return self.indexOf(value) === index;
}
describe("ObjectID", () => {
    test("should be unique in 1 seconds", () => {
        const start = Date.now();
        const ids = new Array<string>();
        while (Date.now() - start < 1000) {
            ids.push(new ObjectID().toString());
        }
        expect(ids.length).toBe(ids.filter(onlyUnique).length);
    })

    test("should make over 10000 in 1 seconds", () => {
        const start = Date.now();
        const ids = new Array<string>();
        while (Date.now() - start < 1000) {
            ids.push(new ObjectID().toString());
        }
        expect(ids.length).toBeGreaterThan(10000);
    })
});