import time
from abc import ABC, abstractmethod
from hashlib import md5
from typing import NewType, TypeVar

KeyHash = NewType('KeyHash', str)
Key = NewType('Key', str)
Value = TypeVar('Value')


class CacheIsFullException(Exception):
    pass


class Node(ABC):
    id: int
    collection: dict[Key, Value]

    @abstractmethod
    def get(self, key: Key) -> Value:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: Key, value: Value) -> None:
        raise NotImplementedError


class CacheServer(Node):
    def __init__(self):
        self.id = time.time_ns()
        self.collection: dict[Key, Value] = {}

    def get(self, key: Key) -> Value:
        return self.collection[key]

    def set(self, key: Key, value: Value) -> None:
        if len(self.collection) > 10:
            raise CacheIsFullException("Cache is full")

        self.collection[key] = value

    def __repr__(self) -> str:
        return str(self.id)


class ConsistentHash:
    def __init__(self, nodes: list[Node], virtual_nodes: int = 100):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring: dict[KeyHash, Node] = {}
        self._generate_ring()

    def _generate_ring(self):
        for node in self.nodes:
            for i in range(self.virtual_nodes):
                key_hash = self._hash(Key(f"{node}:{i}"))
                self.ring[key_hash] = node

    def get_node_by_key(self, key: Key) -> Node:
        if not self.ring:
            raise Exception("No nodes in the ring")
        key_hash = self._hash(key)
        node = self._get_node_by_key_hash(key_hash)
        return node

    def add_node(self, node: Node):
        self.nodes.append(node)
        self._generate_ring()

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self._generate_ring()

    def _get_node_by_key_hash(self, key_hash: KeyHash) -> Node:
        key_hashes = sorted(self.ring.keys())
        if key_hash > key_hashes[-1]:
            return self.ring[key_hashes[0]]
        for _key_hash in key_hashes:
            if key_hash <= _key_hash:
                return self.ring[_key_hash]

    def _hash(self, key: Key) -> KeyHash:
        return KeyHash(md5(key.encode()).hexdigest())
