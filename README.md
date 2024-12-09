# Graphlab Python SDK

## Installation

Requires Python version `^3.8`:

```bash
pip install graphlab
```

## Usage

```py

from graphlab import KnowledgeGraph, Ontology, Entity

g = KnowledgeGraph(
    graphdb='falkordb', # only
    language_model='gpt-4o-mini', # any litellm compatible model supported
)
```
