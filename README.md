# Graphlab Python SDK

## Install

```bash
pip install graphlab
```

## Usage

```py

from graphlab import KnowledgeGraph, Ontology, Entity

g = KnowledgeGraph(
    graphdb='falkordb', # neo4j, falkordb, dgraph currently supported
    language_model='gpt-4o-mini', # any litellm compatible model supported
)

```
