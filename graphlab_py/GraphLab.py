from abc import ABC, abstractmethod
from falkordb import FalkorDB
from neo4j import GraphDatabase

# Abstract base class for graph storage backends
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

# Concrete implementation for Neo4j storage backend
class Neo4jGraphStorage(GraphStorageBackend):
    def __init__(self, connection_details: dict):
        # Initialize Neo4j connection
        uri = connection_details.get('uri', 'bolt://localhost:7687')
        user = connection_details.get('user', 'neo4j')
        password = connection_details.get('password', '')
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_node(self, node_id: str, properties: dict) -> None:
        # Add node to Neo4j
        print(f"Neo4j: Adding node {node_id} with properties {properties}")

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        # Add edge to Neo4j
        print(f"Neo4j: Adding edge from {from_node} to {to_node} with properties {properties}")

    def get_node(self, node_id: str) -> dict:
        # Retrieve node from Neo4j
        print(f"Neo4j: Retrieving node {node_id}")
        return {"id": node_id, "properties": {}}

    def delete_node(self, node_id: str) -> None:
        # Delete node from Neo4j
        print(f"Neo4j: Deleting node {node_id}")

# Concrete implementation for FalkorDB storage backend
class FalkorDBGraphStorage(GraphStorageBackend):
    def __init__(self, connection_details: dict):
        # Initialize FalkorDB connection
        host = connection_details.get('host', 'localhost')
        port = connection_details.get('port', 6379)
        self.client = FalkorDB(host=host, port=port)

    def add_node(self, node_id: str, properties: dict) -> None:
        # Add node to FalkorDB
        print(f"FalkorDB: Adding node {node_id} with properties {properties}")

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        # Add edge to FalkorDB
        print(f"FalkorDB: Adding edge from {from_node} to {to_node} with properties {properties}")

    def get_node(self, node_id: str) -> dict:
        # Retrieve node from FalkorDB
        print(f"FalkorDB: Retrieving node {node_id}")
        return {"id": node_id, "properties": {}}

    def delete_node(self, node_id: str) -> None:
        # Delete node from FalkorDB
        print(f"FalkorDB: Deleting node {node_id}")

# The main Graph interface
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

# # Example usage:
# neo4j_storage = Neo4jGraphStorage(connection_details={})
# graph = GraphInterface(storage_backend=neo4j_storage)

# graph.add_node("1", {"name": "Alice"})
# graph.add_edge("1", "2", {"relationship": "knows"})
# node = graph.get_node("1")
# graph.delete_node("1")
