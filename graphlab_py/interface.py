from .providers import GraphStorageBackend

class Graph:
    def __init__(self, graph: GraphStorageBackend):
        self.graph = graph

    def add_node(self, node_id: str, properties: dict) -> None:
        self.graph.add_node(node_id, properties)

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        self.graph.add_edge(from_node, to_node, properties)

    def get_node(self, node_id: str) -> dict:
        return self.graph.get_node(node_id)
    
    def get_edge(self, from_node: str, to_node: str) -> dict:
        return self.graph.get_edge(from_node, to_node)

    def delete_node(self, node_id: str) -> None:
        self.graph.delete_node(node_id) 

    def delete_edge(self, from_node: str, to_node: str) -> None:
        self.graph.delete_edge(from_node, to_node)
    
    def delete_all(self) -> None:
        self.graph.delete_all()
