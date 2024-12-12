from abc import ABC, abstractmethod

class GraphStorageBackend(ABC):
    @abstractmethod
    def extract_ontology(self) -> dict:
        """Extract the ontology of the graph."""
        pass

    @abstractmethod
    def add_node(self, label: str, node_id: str, properties: dict) -> str:
        """Add a node to the graph.
        
        Args:
            label: Label for the node (e.g., 'Person', 'Project')
            node_id: Unique identifier for the node
            properties: Dictionary of node properties
        """
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
    def get_edge(self, from_node: str, to_node: str) -> dict:
        """Retrieve an edge between two nodes."""
        pass
    
    @abstractmethod
    def delete_node(self, node_id: str) -> None:
        """Delete a node from the graph."""
        pass

    @abstractmethod
    def delete_edge(self, from_node: str, to_node: str) -> None:
        """Delete an edge from the graph."""
        pass

class CypherBasedStorage(GraphStorageBackend):
    @abstractmethod
    def execute_cypher(self, query: str, parameters: dict = None) -> list:
        """Execute a Cypher query and return results."""
        pass

    @abstractmethod
    def extract_ontology(self) -> dict:
        """Extract the ontology of the graph."""
        pass

    def add_node(self, label: str, node_id: str, properties: dict) -> str:
        """Add a node to the graph, avoiding duplicates.

        Args:
            label: Label for the node
            node_id: Unique identifier for the node
            properties: Dictionary of node properties
        """
        props_str = ', '.join(f'n.{k} = ${k}' for k in properties)
        query = (
            f"MERGE (n:{label} {{id: $node_id}}) "
            f"ON CREATE SET {props_str} "
            f"ON MATCH SET {props_str}"
        )
        params = {"node_id": node_id, **properties}
        self.execute_cypher(query, params)
        return node_id

    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        """Add an edge to the graph, updating properties if the edge exists."""
        rel_type = properties.pop('type', 'RELATES_TO').upper()
        props_str = ', '.join(f'r.{k} = ${k}' for k in properties)
        query = (
            f"MATCH (a {{id: $from_node}}), (b {{id: $to_node}}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            f"ON CREATE SET {props_str} "
            f"ON MATCH SET {props_str}"
        )
        params = {"from_node": from_node, "to_node": to_node, **properties}
        self.execute_cypher(query, params)
    
    def get_node(self, node_id: str) -> dict:
        """Retrieve a node by its ID."""
        query = "MATCH (n {id: $node_id}) RETURN n"
        result = self.execute_cypher(query, {"node_id": node_id})
        return self.parse_result(result)
    
    def get_edge(self, from_node: str, to_node: str) -> dict:
        """Retrieve an edge between two nodes."""
        query = """
        MATCH (a {id: $from_node})-[r]->(b {id: $to_node})
        RETURN type(r) as type, properties(r) as properties
        """
        result = self.execute_cypher(query, {"from_node": from_node, "to_node": to_node})
        print(f"get_edge result: {result} from_node: {from_node} to_node: {to_node} query: {query}")
        return self.parse_result(result)
    
    def delete_node(self, node_id: str) -> None:
        """Delete a node from the graph."""
        query = "MATCH (n {id: $node_id}) DETACH DELETE n"
        self.execute_cypher(query, {"node_id": node_id})

    def delete_edge(self, from_node: str, to_node: str) -> None:
        """Delete an edge from the graph."""
        # TODO: this will delete all edges, not good
        query = "MATCH (a {id: $from_node})-[r]->(b {id: $to_node}) DETACH DELETE r"
        self.execute_cypher(query, {"from_node": from_node, "to_node": to_node})

    def flush_graph(self) -> None:
        """Delete all nodes and edges from the graph."""
        self.execute_cypher("MATCH (n) DETACH DELETE n")
        self.execute_cypher("MATCH ()-[r]->() DETACH DELETE r")
        
    def parse_result(self, result: list) -> dict:
        """Parse the result of a Cypher query."""
        return result
