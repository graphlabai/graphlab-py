# Plan

- lage et lib som gjør det enklere å lage KGs med LLMS
- en wrapper over falkordb og neo4j python sdk's, som kan inneholde shortcuts som passer våre prosjekter
- funksjonalitet for server, api, chat ui

### Publish package

```bash
rm -rf dist
poetry build
twine upload dist/*
```

# Architecture

## RETRIEVAL

Agents that talk to each other, determining what is needed:
-> (0) ENTRY agent. Will control flow <->. Passing first to:

-> (1) guard against misuse, scope, boundaries.
-> (0) continue

-> (2) agent that refines question, using environment context (eg. "I'm working in an architecture firm."), considerin the graph schema and some sample data, other available sources, consider also chat history. perhaps ask for clarification. pass this enriched question back to 0,
-> (0) which will pass it on to:

-> (3) agent that considers what data sources are available and which of them could be relevant. may be eg. one or several graphs, Internet, other DBs, or none. Perhaps request includes instructions about sources.
-> (0) Pass question over to each data agent:

-> (4a) GRAPH agent. Considers pre-defined Cypher queries, if they are relevant.
... Considers graph schema, sample data.
... Creates Cypher query to pull data from graph. Uses {function_call} to fetch data.
... Could run in multiple steps: if vector search, get nodes, fetch surrounding nodes, find the relevant one. Then do another follow up query around this node. Etc...
-> (4b) Internet agent. Considers query, fetches data from internet search, scrape.
-> (4c) Postgres agent.
-> (4d) VectorDB agent.
-> (4e) Wikidata agent. Lots of other possible APIs. (Weather, Financial, literally thousands. Tools already exist for this.)
-> (4f) Microsoft Graph.
-> (0) Send all results to agent for reranking, evaluation

-> (5) Reranking of data, evaluation of data. Is it enough? Should we ask for more graph data? Now that we know the answer, can we enrich it?
... Is it better to ask LLM to rerank without knowing question? OR should it re-rank knowing the question, but not answer it?
... Should it summarize?
... Remove irrelevant context
... Send re-ranked context back to 0.
... Possible with a loop here: If more data needed, send back to (2)..?
-> (0) Send re-ranked context to Answering Agent:

-> (6) Answer question, summarise, write it up nice, perhaps following a template.
... Perhaps multiple answer agents, depending on type of request. One can write a propsal using a template and guideline, one can write other styles, etc.
-> (0) Return answer to client.

- Total: 6 types of agents:
  ##########################

  0. CONDUCTOR agent
  1. GUARD DOG agent:
  2. REFINING agent
  3. DATA SOURCE PICKER agent: Knows which data sources we have, with summary and schema for what they contain. Determine which data sources are relevant to our request.
  4. DATA agent(s): Fetch data from different data sources. Need to separate LLM vs functions here:
     4.1 LLM to create query,
     4.2 function to fetch data. (Tools cannot fetch data, must happen locally, while tools are run in LLM provider's cloud.)
  5. RERANKER agent: Given lots of context and a question, clean up the context, rerank data, remove superfluous data. Ensure references to data sources are kept.
  6. ANSWER agent: Given request, context, possible template and guidelines, will write up a pretty answer, with proper references.

#### Refinements

- keeping references to pieces of context along the way
- automatic retry on failed LLM calls
- use of pydantic response_formats
- more loops: if more data needed, request more data. eg. Cypher query might fail (could be syntax, could be bad query returning no/bad data), so retry with an improved query. etc.
- external logging
- intermediate replies to client? (Hold on, working on it...etc)

## KNOWLEDGE GRAPH BUILDER

Again agents that talk to each other, handling different parts of the task.

- different roads:
  - one is to create a KG from scratch, based on a trove of data.
  - second is to add to an existing KG.
  - if ontology is already defined, then they are more or less the same.
  - if ontology is to be auto-generated, then a larger dataset is needed up front.
- would be great to have a way of chatting with the KG structure:
  - doing deduplication as an interactive exercise
  - creating new entities, perhaps removing others.
  - chatting: i want an ontology with these nodes, and these edges, etc.
- also have systems that massage the KG, looking for duplicates, etc... (later roadmap)
- say we have ontology, we then add our sources:
  - could be pdfs
  - could be urls
  - could be csv
  - could be emails
  - could be chat messages (eg. "Anna is working on Project B starting today.")
- agents that read each type of source, get the raw data
- agent that refines the data, picks out what's relevant?
- agent that creates a list of the ENTITIES, attributes, RELATIONS in the data
- agent that creates a schema from the list
- agent that checks if it already exists in the graph? how this new data fits in with existing.
- fn that takes the schema and creates Cypher programmatically and adds entries to the KG

### Flow

- Instantiate KnowledgeGraph Class
- add Ontology, either as JSON or as LLM chat description -> JSON. See FalkorDB or Neo4j python drivers for inspo.
- could also connect to existing Graph (non-empty database) and extract ontology
- request data import: kg.add_data(pdf | url | csv)
- this starts the team effort:
  - Agent 1: Read data source, clean it up, structure it reasonably well, add section with reference pointers.
  - Agent 2: Read cleaned data, create ENTITIES and RELATIONS with attributes based on the data and pre-defined Ontology. Output some JSON schema
  - Agent 3: Check the Entities and Rels against existing? Or just MERGE?
  - Agent 4:

## KG

- Would be nice to support multiple graph backends. Expose general methods, that are implemented differently for each backend: FalkorDB, Kuzu, Neo4j, DGraph, Apache AGE, etc.
- Hvilke metoder trenger vi?
  - Strengt tatt bare å sende Cypher query? Resten kan være generelt? (Men det betyr at man ikke kan bruke apoc...men det er OK.)
  - Så alle graph backeds som tar Cypher er like, bare forskjellig config / connection.

## LLM

- Support any LLM, so using LiteLLM

## API

- Using FastAPI to expose an API for chat, etc.

---

# Usage

```py

from graphlab_py import KnowledgeGraph, FalkorDBConfig
from graphlab_py.sources


config = FalkorDBConfig(
  host='localhost',
  port='6379',
)

kg = KnowledgeGraph(
  config=config
)

# select the 'people' graph
kg.select_graph('people')

# get info on graph
kg.get_info() # returns metainfo, like how many nodes, entities, name, etc.

# add data to graph






```
