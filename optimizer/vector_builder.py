import os
from crewai_tools import RagTool
from optimizer.utils.vector_utils import is_valid_chroma_vector_db


class VectorDbBuilder:
    def __init__(
        self,
        knowledge_base_abspath: str,
        vector_db_abspath: str,
        embedding_model: str = "text-embedding-ada-002",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        force_rebuild: bool = False,
    ):
        self.knowledge_base_path = knowledge_base_abspath
        self.vector_db_path = vector_db_abspath
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.force_rebuild = force_rebuild

    def build_if_needed(self) -> None:
        if self.force_rebuild or not is_valid_chroma_vector_db(self.vector_db_path):
            print("🛠️ Building or rebuilding vector DB from knowledge base...")
            self._build_vector_db()
        else:
            print("📦 Using existing vector DB at:", self.vector_db_path)

    def _build_vector_db(self) -> None:
        rag_tool = RagTool(
            config=dict(
                embedder=dict(
                    provider="openai",
                    config=dict(model=self.embedding_model),
                ),
                chunker=dict(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                ),
                vectordb=dict(
                    provider="chroma",
                    config=dict(
                        dir=self.vector_db_path,
                        collection_name="knowledge_base",
                        allow_reset=True,
                    ),
                ),
            )
        )

        if not os.path.exists(self.knowledge_base_path):
            raise FileNotFoundError(
                f"Knowledge base not found at: {self.knowledge_base_path}"
            )

        rag_tool.add(self.knowledge_base_path, data_type="directory")

    def get_vector_db_abspath(self) -> str:
        return self.vector_db_path
