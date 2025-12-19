from shared.embedder import KnowledgeBaseEmbedder
from config.settings import get_config


def embed_kb():
    """Rebuild the vector database from the knowledge base documents"""
    config = get_config()
    embedder = KnowledgeBaseEmbedder(
        knowledge_base_abspath=config.knowledge_base_abspath,
        vector_db_abspath=config.vector_db_abspath,
        force_rebuild=True,
    )
    embedder.build_if_needed()
