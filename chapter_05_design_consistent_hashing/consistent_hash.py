from abc import ABC, abstractmethod
from collections import Counter
from hashlib import md5
from typing import NewType, TypeVar
from uuid import uuid4

KeyHash = NewType("KeyHash", str)
Key = NewType("Key", str)
Value = TypeVar("Value")


class CacheIsFullException(Exception):
    pass


class KeyDoesNotExistException(Exception):
    pass


class MaxNodesSizeException(Exception):
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
        self.id = uuid4().int
        self.collection: dict[Key, Value] = {}
        self._MAX_SIZE = 10

    def get(self, key: Key) -> Value:
        value = self.collection.get(key, None)
        if value is None:
            raise KeyDoesNotExistException("Key does not exist")
        return value

    def set(self, key: Key, value: Value, force: bool = False) -> None:
        if not force and len(self.collection) >= self._MAX_SIZE:
            raise CacheIsFullException("Cache is full")

        self.collection[key] = value

    def __repr__(self) -> str:
        return str(self.id)


class ConsistentHash:
    def __init__(self, nodes: list[Node], virtual_nodes: int = 2000):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring: dict[KeyHash, Node] = {}
        self._generate_ring()
        self._MAX_SIZE = 3

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

    def _get_node_by_key_hash(self, user_key_hash: KeyHash) -> Node:
        key_hashes = sorted(self.ring.keys())

        if user_key_hash > key_hashes[-1]:
            return self.ring[key_hashes[0]]

        for _key_hash in key_hashes:
            if user_key_hash <= _key_hash:
                return self.ring[_key_hash]

    def add_node(self, node: Node):
        if len(self.nodes) >= self._MAX_SIZE:
            raise MaxNodesSizeException("Max nodes size reached")
        self.nodes.append(node)
        self._generate_ring()

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self._generate_ring()

    def _hash(self, key: Key) -> KeyHash:
        return KeyHash(md5(key.encode()).hexdigest())

    @property
    def number_of_nodes(self) -> int:
        return len(self.nodes)

    @property
    def node_ids(self) -> list[int]:
        return [node.id for node in self.nodes]

    @property
    def ring_info(self) -> list[str]:
        counter = Counter(self.ring.values())
        return [f"{node.id}:{counter[node]}" for node in self.nodes]
