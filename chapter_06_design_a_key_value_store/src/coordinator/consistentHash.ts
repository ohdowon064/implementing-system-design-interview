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
  private nodes: Node[];
  private numberOfVirtualsPerNode = 100;

  constructor(nodes: Node[]) {
    this.nodes = nodes;
    this.ring = new Map<number, Node>();
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
    const index = keys.findIndex((value) => value >= hash);
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
