# Architecture Notes

## Candidate Profiler Tool Architecture Summary

### RagTool

Give the agent a `RagTool` that

- uses existing ChromaDB vector store if available
- builds the vector store from kb docs if missing or invalid
- separates concerns of embedding and querying
- uses configurable LLM for semantic retrieval

#### Components

##### `utils/vector_utils.py`

- validates ChromDB vector store
- can clobber a vector store
- can print vector DB info

##### `VectorDbBuilder`

- handles vector DB creation
- skips creation if valid DB exists
- supports forced rebuilds

##### `get_rag_tool` function in `agents.py`

- uses the components above to manage and validate the vector store

### DirectoryReadTool

Give the agent access to the knowledge base directory to

- retrieve full documents when a semantic chunk is interesting but incomplete
- understand project or skill context beyond summarized chroma-embeddings
- bridge RAG output with original source materials
