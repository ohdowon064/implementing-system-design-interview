from hashlib import md5


class CacheServer:
    def __init__(self, _id: int):
        self.id = _id
        self._collection = {}

    def get(self, key):
        return self._collection[key]

    def set(self, key, value):
        self._collection[key] = value

    def __repr__(self):
        return str(self.id)


class ConsistentHashWithVirtualNode:
    def __init__(self, nodes: list[CacheServer], virtual_nodes: int = 100):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring: dict[str, CacheServer] = {}
        self._generate_ring()

    def _generate_ring(self):
        for node in self.nodes:
            for i in range(self.virtual_nodes):
                key = self._hash("{}:{}".format(node, i))
                self.ring[key] = node

    def get_node(self, key) -> CacheServer:
        if not self.ring:
            raise Exception("No nodes in the ring")
        key_hash = self._hash(key)
        node = self._get_node(key_hash)
        return node

    def add_node(self, node):
        self.nodes.append(node)
        self._generate_ring()

    def _get_node(self, key_hash) -> CacheServer:
        keys = sorted(self.ring.keys())
        if key_hash > keys[-1]:
            return self.ring[keys[0]]
        for k in keys:
            if key_hash <= k:
                return self.ring[k]

    def _hash(self, key) -> str:
        return md5(key.encode()).hexdigest()


def test_consistent_hash_with_assert():
    nodes = []
    for i in range(10):
        nodes.append(CacheServer(i))
