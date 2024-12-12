from .providers import GraphStorageBackend

class Graph:
    def __init__(self, engine: GraphStorageBackend):
        self._graph = engine

    def extract_ontology(self) -> dict:
        return self._graph.extract_ontology()

    def add_node(self, label: str, node_id: str, properties: dict) -> str:
        """Add a node to the graph.
        
        Args:
            label: Label for the node (e.g., 'Person', 'Project')
            node_id: Unique identifier for the node
            properties: Dictionary of node properties
        
        Returns:
            str: The node_id of the created node
        """
        self._graph.add_node(label, node_id, properties)
        return node_id

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        """Add an edge between two nodes.
        
        Args:
            from_node: The node_id of the source node
            to_node: The node_id of the target node
            properties: Dictionary of edge properties
        """
        self._graph.add_edge(from_node, to_node, properties)

    def get_node(self, node_id: str) -> dict:
        return self._graph.get_node(node_id)
    
    def get_edge(self, from_node: str, to_node: str) -> dict:
        return self._graph.get_edge(from_node, to_node)

    def delete_node(self, node_id: str) -> None:
        self._graph.delete_node(node_id) 

    def delete_edge(self, from_node: str, to_node: str) -> None:
        self._graph.delete_edge(from_node, to_node)
    
    def flush_graph(self) -> None:
        self._graph.flush_graph()
