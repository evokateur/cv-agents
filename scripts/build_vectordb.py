from optimizer.vector_builder import VectorDbBuilder
from config import get_config

builder = VectorDbBuilder(
    knowledge_base_abspath=get_config().knowledge_base_abspath,
    vector_db_abspath=get_config().vector_db_abspath,
    force_rebuild=False,
)

builder.build_if_needed()
