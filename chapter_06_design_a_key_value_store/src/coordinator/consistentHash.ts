class Node {
  id: number;
  collection: Map<number, string>;

  constructor(id: number) {
    this.id = id;
    this.collection = new Map<number, string>();
  }

  put(key: number, value: string) {
    this.collection.set(key, value);
  }

  get(key: number) {
    return this.collection.get(key);
  }
}

export class ConsistentHash {
  private ring: Map<number, Node>;
}
