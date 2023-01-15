import { Injectable } from '@nestjs/common';
import { ConsistentHash, Node } from './consistentHash';
@Injectable()
export class CoordinatorService {
  nodes: Node[] = [new Node(1), new Node(2), new Node(3)];
  consistentHash: ConsistentHash = new ConsistentHash(this.nodes);

  put(key: string, value: string): void {
    const node = this.consistentHash.findNodeByKey(key);
    node.put(key, value);
  }

  get(key: string): string {
    const node = this.consistentHash.findNodeByKey(key);
    const value = node.get(key);
    if (value === undefined) {
      return null;
    }
    return value;
  }
}
