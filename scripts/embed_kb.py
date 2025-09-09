import sys

sys.path.append(".")

from optimizer.knowledge_embedder import KnowledgeBaseEmbedder
from config import get_config

embedder = KnowledgeBaseEmbedder(
    knowledge_base_abspath=get_config().knowledge_base_abspath,
    vector_db_abspath=get_config().vector_db_abspath,
    force_rebuild=True,
)

embedder.build_if_needed()
