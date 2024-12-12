from neo4j import GraphDatabase
from .base import CypherBasedStorage


class OntologyExtractor:

    def __init__(self, client):
        """
        Initialize with an existing Neo4j client object.
        :param client: A Neo4j client object with an `execute_cypher` method.
        """
        self.client = client

    def extract_ontology(self):
        """
        Extracts the ontology from the Neo4j graph.
        :return: A dictionary containing node labels, relationship types, and mappings.
        """
        labels = self._get_node_labels()
        relationships = self._get_relationship_types()
        mappings = self._get_relationship_mappings()
        return {
            "labels": labels,
            "relationships": relationships,
            "mappings": mappings
        }

    def _get_node_labels(self):
        """
        Retrieves all node labels in the database.
        :return: A list of node labels.
        """
        query = "CALL db.labels()"
        result = self.client.execute_cypher(query)
        return [record["label"] for record in result]

    def _get_relationship_types(self):
        """
        Retrieves all relationship types in the database.
        :return: A list of relationship types.
        """
        query = "CALL db.relationshipTypes()"
        result = self.client.execute_cypher(query)
        return [record["relationshipType"] for record in result]

    def _get_relationship_mappings(self):
        """
        Maps relationships between node types and their frequencies.
        :return: A list of dictionaries with relationship mappings.
        """
        query = """
        MATCH (a)-[r]->(b)
        RETURN 
            labels(a) AS StartNodeLabels, 
            type(r) AS RelationshipType, 
            labels(b) AS EndNodeLabels, 
            count(*) AS Frequency
        ORDER BY Frequency DESC
        """
        result = self.client.execute_cypher(query)
        return [
            {
                "startNodeLabels": record["StartNodeLabels"],
                "relationshipType": record["RelationshipType"],
                "endNodeLabels": record["EndNodeLabels"],
                "frequency": record["Frequency"]
            }
            for record in result
        ]

class Neo4jGraphStorage(CypherBasedStorage):
    def __init__(self, host: str, port: int = 7687, user: str = "neo4j", password: str = "", name: str = "default"):
        self.client = GraphDatabase.driver(f"neo4j://{host}:{port}", auth=(user, password))

    def execute_cypher(self, query: str, parameters: dict = None) -> list:
        with self.client.session() as session:
            result = session.run(query, parameters or {})
            return list(result)

    def extract_ontology(self):
        return OntologyExtractor(self).extract_ontology()

    def parse_result(self, result: list) -> dict:
        print(f"parse_result result: {result}")
        return [record.data() for record in result]

    def get_edge(self, from_node: str, to_node: str) -> dict:
        """Retrieve an edge between two nodes."""
        query = """
        MATCH 
            (a {id: $from_node})
            -[r]->
            (b {id: $to_node})
        RETURN 
            type(r) as type, 
            properties(r) as properties, 
            a as from_node, 
            b as to_node, 
            r as edge
        """
        result = self.execute_cypher(query, {"from_node": from_node, "to_node": to_node})
        return self.parse_result(result)
    
