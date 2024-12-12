from falkordb import FalkorDB, Graph
from .base import CypherBasedStorage

class FalkorDBGraphStorage(CypherBasedStorage):
    def __init__(self, host: str, port: int, name: str):
        self.client = FalkorDB(host=host, port=port)
        self.select_graph(name)
    
    def execute_cypher(self, query: str, parameters: dict = None) -> list:
        return self._graph.query(query, parameters or {})
    
    def extract_ontology(self) -> dict:
        return self._graph.get_schema()

    def select_graph(self, name: str) -> Graph:
        self._graph = self.client.select_graph(name)
        return self._graph
    
    def parse_result(self, result) -> dict:
        if not hasattr(result, 'result_set'):
            return None

        if not result.result_set:
            return None
            
        row = result.result_set[0]
        
        return row[0] if row else None
