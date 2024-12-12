from neo4j import GraphDatabase
from .base import CypherBasedStorage

class Neo4jGraphStorage(CypherBasedStorage):
    def __init__(self, host: str, port: int = 7687, user: str = "neo4j", password: str = "", name: str = "default"):
        self.client = GraphDatabase.driver(f"neo4j://{host}:{port}", auth=(user, password))

    def execute_cypher(self, query: str, parameters: dict = None) -> list:
        with self.client.session() as session:
            result = session.run(query, parameters or {})
            return list(result)

    def parse_result(self, result: list) -> dict:
        return [record.data() for record in result]
