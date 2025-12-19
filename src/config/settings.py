import os
from pathlib import Path
from pydantic import BaseModel
from shared.config import RagSettings, ChatSettings, PathSettings, BaseConfig, load_yaml_config


class Settings(BaseModel):
    """Shared configuration model for RAG, chat, and paths"""
    rag: RagSettings
    chat: ChatSettings
    paths: PathSettings


class Config(BaseConfig):
    def __init__(self):
        super().__init__(Path(__file__).parent, Settings)

    @property
    def knowledge_base_abspath(self) -> str:
        return os.path.abspath(self._settings.paths.knowledge_base)

    @property
    def vector_db_abspath(self) -> str:
        return os.path.abspath(self._settings.paths.vector_db)


def get_config() -> Config:
    """Get shared configuration"""
    return Config()


def get_rag_config() -> dict:
    """Get RAG configuration from YAML, validated with Pydantic"""
    config_dir = Path(__file__).parent
    yaml_config = load_yaml_config(config_dir)
    settings = Settings(**yaml_config)

    return {
        "embedding_model": settings.rag.embedding_model,
        "collection_name": settings.rag.collection_name,
        "num_results": settings.rag.num_results,
        "chunk_size": settings.rag.chunk_size,
        "chunk_overlap": settings.rag.chunk_overlap,
    }


def get_chat_config() -> dict:
    """Get chat configuration from YAML, validated with Pydantic"""
    config_dir = Path(__file__).parent
    yaml_config = load_yaml_config(config_dir)
    settings = Settings(**yaml_config)

    return {
        "model": settings.chat.model,
        "temperature": settings.chat.temperature,
    }
