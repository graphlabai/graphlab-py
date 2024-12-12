from .storage.base import GraphStorageBackend

class GraphInterface:
    def __init__(self, storage_backend: GraphStorageBackend):
        self.storage_backend = storage_backend

    def add_node(self, node_id: str, properties: dict) -> None:
        self.storage_backend.add_node(node_id, properties)

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        self.storage_backend.add_edge(from_node, to_node, properties)

    def get_node(self, node_id: str) -> dict:
        return self.storage_backend.get_node(node_id)

    def delete_node(self, node_id: str) -> None:
        self.storage_backend.delete_node(node_id) 