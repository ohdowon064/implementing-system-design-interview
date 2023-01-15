import { Injectable } from '@nestjs/common';
import { ConsistentHash, Node } from './consistentHash';
@Injectable()
export class CoordinatorService {
  nodes: Node[] = [new Node(1), new Node(2), new Node(3)];
  consistentHash: ConsistentHash = new ConsistentHash(this.nodes);

  put(key: string, value: string): void {
    console.log('coordinate put 호출됨');
    console.log(this.consistentHash.ring);
    console.log(value);

    const node = this.consistentHash.findNodeByKey(key);
    console.log(node);
    console.log(node.collection);
    node.put(key, value);
    console.log(node);
  }

  get(key: string): string {
    console.log('coordinate get 호출됨');
    console.log(this.consistentHash.ring);
    const node = this.consistentHash.findNodeByKey(key);
    const value = node.get(key);
    if (value === undefined) {
      return null;
    }
    return value;
  }
}
