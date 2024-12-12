# Graphlab Python SDK

## Installation

Requires Python version `^3.8`:

```bash
pip install graphlab-py
```

## Usage

```py
from graphlab_py import KnowledgeGraph

g = KnowledgeGraph()
```

## Graph Backend

#### Neo4J Docker

```bash
docker volume create neo4j_data
docker run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/your_password \
    --volume=neo4j_data:/data \
    --rm \
    neo4j:5.26.0
```

#### FalkorDB Docker

```bash
docker volume create falkordb_data
docker run \
    --restart always \
    -p 6379:6379 \
    -p 3000:3000 \
    --volume falkordb_data:/data \
    --rm \
    falkordb/falkordb:edge
```
