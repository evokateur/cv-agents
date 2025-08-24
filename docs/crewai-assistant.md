# Q&A with CrewAI assistant

---

> Is there a standard directory where agents will look for knowledge or is it configurable?

Based on the search results, here's what I found about knowledge directory locations in CrewAI:

Standard Directory: Yes, there is a standard directory. CrewAI uses KNOWLEDGE_DIRECTORY (usually "knowledge") as the default location for knowledge files.

It's Configurable: You can customize the storage location using the CREWAI_STORAGE_DIR environment variable:

```python
import os
os.environ["CREWAI_STORAGE_DIR"] = "./my_project_storage"
# All knowledge will now be stored in ./my_project_storage/knowledge/
```

Default Locations by Platform:

    macOS: ~/Library/Application Support/CrewAI/{project_name}/knowledge/
    Linux: ~/.local/share/CrewAI/{project_name}/knowledge/
    Windows: C:\Users\{username}\AppData\Local\CrewAI\{project_name}\knowledge\

To Check Your Current Location:

```python
from crewai.utilities.constants import KNOWLEDGE_DIRECTORY
from crewai.utilities.paths import db_storage_path
import os

knowledge_path = os.path.join(db_storage_path(), "knowledge")
print(f"Knowledge storage location: {knowledge_path}")
```

---

>What is the knowledge directory's main function?

Based on the search results, the knowledge directory's main function is to:

Store and manage knowledge sources for CrewAI agents to query and retrieve relevant information during task execution.

Key Functions:

    Content Storage: Stores processed knowledge from various sources (PDFs, CSVs, web pages, etc.) in collections
    Query Processing: When agents execute tasks, it automatically transforms task prompts into optimized search queries using the _get_knowledge_search_query method
    Information Retrieval: Provides contextually relevant information to agents based on their current tasks
    Collection Management: Organizes knowledge into named collections (defaults to "knowledge" collection)

How it Works:

    Knowledge sources are processed and stored in the directory
    During task execution, agents automatically query this knowledge base
    The LLM transforms the original task into an optimized search query
    Relevant information is retrieved and provided to the agent

The knowledge directory essentially acts as a dynamic, queryable knowledge base that enhances agent capabilities by providing access to domain-specific information without requiring model retraining.

---

>What is the best way to configure a RagAgent that will use an existing ChromaDB vector database?

Based on the search results, here's the best way to configure a RagAgent that uses an existing ChromaDB vector database:

Configure RagTool with ChromaDB:

```python
from crewai_tools import RagTool

# Configure RagTool to use existing ChromaDB
config = {
    "vectordb": {
        "provider": "chroma",
        "config": {
            "collection_name": "your-existing-collection",
            "dir": "/path/to/your/existing/chromadb",  # Path to existing ChromaDB
            "allow_reset": False  # Prevent overwriting existing data
        }
    },
    "llm": {
        "provider": "openai",
        "config": {"model": "gpt-4"}
    },
    "embedding_model": {
        "provider": "openai",
        "config": {"model": "text-embedding-ada-002"}
    }
}

rag_tool = RagTool(config=config)

@agent
def rag_agent(self) -> Agent:
    return Agent(
        config=self.agents_config["rag_agent"],
        tools=[rag_tool]
    )
```

---

>If you want the same agent that queries the vector DB to search unchunked docs (the source of the embeddings) in a specific directory what's the best sort of tool to use, and how and where does the prompt go in the YAML (agent or task)?

For searching unchunked documents in a directory, the DirectorySearchTool is the best choice. It performs semantic RAG search across all files in a directory.

Where the prompt goes:

    Agent prompts (role, goal, backstory) go in agents.yaml
    Task prompts (description, expected_output) go in tasks.yaml

Example setup:

```python
from crewai_tools import RagTool, DirectorySearchTool

# Vector DB tool for embeddings
rag_tool = RagTool(config={
    "vectordb": {"provider": "chroma", "config": {"dir": "/path/to/chromadb"}}
})

# Directory search for unchunked docs
directory_tool = DirectorySearchTool(directory='/path/to/source/docs')

@agent
def research_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['research_agent'],
        tools=[rag_tool, directory_tool]
    )
```

YAML configuration:

```yaml
# agents.yaml
research_agent:
  role: Research Analyst
  goal: Search both vector database and source documents
  backstory: Expert at finding information from multiple sources

# tasks.yaml  
research_task:
  description: |
    Search the vector database for relevant embeddings, then search 
    the original documents in {source_directory} for additional context
  expected_output: Comprehensive analysis from both sources
  agent: research_agent
```
