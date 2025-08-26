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

## Putting Pydantic Schema in Prompts

>"*It was sending the bones!*"

The vector database was being created correctly, but the candidate profiler
was not using it correctly. It was taking the structured output it received and
sending chunks of it as queries. The RAG tool expects natural language
language queries for semantic search. Prompting it to use natural language
wasn't going to fix the problem, since it didn't know where to look for meaning[^1].
All it could do was send random parts (unnatural queries) and hope for the best.

[^1]: The CrewAI Assistant says a very sophisticated model could pull it off
(but we get what we pay for, around here).

To fix this we have to create the task description dynamically, injecting
the relevant schema information for any task that receives structured output
from the previous task[^2].

[^2]: An `input_pydantic` parameter exists but setting it does not expose the
schema to the agent. It's only used for validation (and cannot specify more
than one type).  

The description starts as a template with placeholders for the schema, then
it's sent to a helper function that injects the Pydantic schema information
in right places, i.e. `[[JobPosting]]`. I chose those delimiters so future
me will not confuse them with the normal sort of variable placeholders found
in task descriptions.

YAML is still used for the tasks, with a temporary description indicating
what's to come.

New thing:

#### `utils/prompt_utils.py`

- a function to inject a Pydantic schema into text
- a function to fill all placeholders in a block of text
