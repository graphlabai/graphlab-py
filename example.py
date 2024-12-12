from graphlab_py.providers import FalkorDBGraphStorage, Neo4jGraphStorage
from graphlab_py import Graph

falkor_engine = FalkorDBGraphStorage(
    host="localhost",
    port=6379,
    name="test-2"
)

neo4j_engine = Neo4jGraphStorage(
    host="localhost",
    port=7687,
    user="neo4j",
    password="your_password",
    name="test-2"
)

# g = Graph(engine=falkor_engine)
g = Graph(engine=neo4j_engine)

# # g.flush_graph()

# project_1 = g.add_node("Project", "project_1", {"name": "Project Paradise"})
# person_2 = g.add_node("Person", "person_2", {"name": "Jane"})
# person_3 = g.add_node("Person", "person_3", {"name": "Tarzan"})

# g.add_edge(person_2, project_1, {"type": "works_on", "role": "developer", "start_date": "2024-01-01"})
# g.add_edge(person_3, project_1, {"type": "works_on", "role": "project_manager"})

print(g.extract_ontology())