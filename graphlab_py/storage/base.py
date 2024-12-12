from abc import ABC, abstractmethod

class GraphStorageBackend(ABC):
    @abstractmethod
    def add_node(self, node_id: str, properties: dict) -> None:
        """Add a node to the graph."""
        pass

    @abstractmethod
    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        """Add an edge to the graph."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> dict:
        """Retrieve a node by its ID."""
        pass

    @abstractmethod
    def delete_node(self, node_id: str) -> None:
        """Delete a node from the graph."""
        pass
