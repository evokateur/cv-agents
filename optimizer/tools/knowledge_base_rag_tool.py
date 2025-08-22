import os
from crewai_tools import RagTool
from config import get_config


def create_knowledge_base_rag_tool() -> RagTool:
    config = get_config()

    rag_tool = RagTool(
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model=config.candidate_profiler_model,
                    temperature=float(config.candidate_profiler_temperature),
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model="text-embedding-ada-002",
                ),
            ),
            chunker=dict(
                chunk_size=1000,
                chunk_overlap=200,
            ),
            vectordb=dict(
                provider="chroma",
                config=dict(
                    dir=os.path.abspath("vector_db"),
                    collection_name="knowledge_base",
                    allow_reset=True,  # Recreate vector DB each time for fresh data
                ),
            ),
        )
    )

    knowledge_base_path = os.path.abspath("knowledge-base")

    if not os.path.exists(knowledge_base_path):
        raise FileNotFoundError(
            f"Knowledge base directory not found: {knowledge_base_path}"
        )

    rag_tool.add(knowledge_base_path, data_type="directory")

    return rag_tool


knowledge_base_rag_tool = create_knowledge_base_rag_tool()
