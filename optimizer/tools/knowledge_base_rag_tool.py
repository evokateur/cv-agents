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
                    allow_reset=False,  # Don't reset production DB
                ),
            ),
        )
    )

    # Ensure knowledge base documents are loaded
    knowledge_base_path = os.path.abspath("knowledge-base")
    if os.path.exists(knowledge_base_path):
        try:
            rag_tool.add(knowledge_base_path, data_type="directory")
        except Exception as e:
            # Handle case where documents are already loaded
            if "existing embedding ID" not in str(e):
                raise e

    return rag_tool


# Export singleton instance
knowledge_base_rag_tool = create_knowledge_base_rag_tool()
