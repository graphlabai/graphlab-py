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

    def add_node(self, node_id: str, properties: dict) -> None:
        """Add a node to the graph."""
        props_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"CREATE (n:Node {{id: $node_id, {props_str}}})"
        params = {"node_id": node_id, **properties}
        self.execute_cypher(query, params)
    
    def add_edge(self, from_node: str, to_node: str, properties: dict) -> None:
        """Add an edge to the graph."""
        props_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = """
        MATCH (a:Node {id: $from_node}), (b:Node {id: $to_node})
        CREATE (a)-[r:RELATES_TO {%s}]->(b)
        """ % props_str
        params = {
            "from_node": from_node,
            "to_node": to_node,
            **properties
        }
        self.execute_cypher(query, params)
    
    def get_node(self, node_id: str) -> dict:
        """Retrieve a node by its ID."""
        query = "MATCH (n:Node {id: $node_id}) RETURN n"
        result = self.execute_cypher(query, {"node_id": node_id})
        return self.parse_result(result)
    
    def get_edge(self, from_node: str, to_node: str) -> dict:
        """Retrieve an edge between two nodes."""
        query = """
        MATCH (a:Node {id: $from_node})-[r:RELATES_TO]->(b:Node {id: $to_node})
        RETURN r
        """
        result = self.execute_cypher(query, {"from_node": from_node, "to_node": to_node})
        return self.parse_result(result)
    
    def delete_node(self, node_id: str) -> None:
        """Delete a node from the graph."""
        query = "MATCH (n:Node {id: $node_id}) DETACH DELETE n"
        self.execute_cypher(query, {"node_id": node_id})

    def delete_edge(self, from_node: str, to_node: str) -> None:
        """Delete an edge from the graph."""
        query = "MATCH ()-[r]->() WHERE r.from_node = $from_node AND r.to_node = $to_node DETACH DELETE r"
        self.execute_cypher(query, {"from_node": from_node, "to_node": to_node})

    def delete_all(self) -> None:
        """Delete all nodes and edges from the graph."""
        self.execute_cypher("MATCH (n) DETACH DELETE n")
        self.execute_cypher("MATCH ()-[r]->() DETACH DELETE r")
        
    def parse_result(self, result: list) -> dict:
        """Parse the result of a Cypher query."""
        return result
