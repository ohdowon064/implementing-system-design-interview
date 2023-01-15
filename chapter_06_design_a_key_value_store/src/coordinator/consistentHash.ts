export class Node {
  id: number;
  collection: Map<string, string>;

  constructor(id: number) {
    this.id = id;
    this.collection = new Map<string, string>();
  }

  put(key: string, value: string): void {
    this.collection.set(key, value);
  }

  get(key: string): string {
    const value = this.collection.get(key);
    return value;
  }
}

export class ConsistentHash {
  public ring: Map<number, Node>;
  private nodes: Node[];
  private numberOfVirtualsPerNode = 10;

  constructor(nodes: Node[]) {
    this.nodes = nodes;
    this.ring = new Map<number, Node>();
    this.generateRing();
  }

  generateRing(): void {
    for (const index in this.nodes) {
      for (let i = 0; i < this.numberOfVirtualsPerNode; i++) {
        const hash = this.hash(index + i);
        this.ring.set(hash, this.nodes[index]);
      }
    }
  }

  findNodeByKey(key: string): Node {
    const hash = this.hash(key);
    const keys = Array.from(this.ring.keys());
    console.log(hash);
    const index = keys.findIndex((value) => value >= hash);
    if (index === -1) {
      return this.ring.get(keys[0]);
    }
    return this.ring.get(keys[index]);
  }

  addNode(node: Node): void {
    this.nodes.push(node);
    this.generateRing();
  }

  removeNode(node: Node): void {
    this.nodes = this.nodes.filter((value) => value.id !== node.id);
    this.generateRing();
  }

  hash(key: string): number {
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      hash = (hash << 5) - hash + key.charCodeAt(i);
      hash &= hash;
    }
    return hash;
  }
}
