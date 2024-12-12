from graphlab_py.providers import FalkorDBGraphStorage, Neo4jGraphStorage
from graphlab_py import Graph

# backend = FalkorDBGraphStorage(
#     host="localhost",
#     port=6379,
#     name="test-2"
# )

backend = Neo4jGraphStorage(
    host="localhost",
    port=7687,
    user="neo4j",
    password="your_password",
    name="test-2"
)

print(backend)


graph = Graph(backend)


print(graph)

graph.delete_all()

graph.add_node("1", {"name": "John"})
graph.add_node("2", {"name": "Jane"})
graph.add_edge("1", "2", {"type": "friend"})

print(graph.get_node("1"))
print(graph.get_node("2"))
print(graph.get_edge("1", "2"))

