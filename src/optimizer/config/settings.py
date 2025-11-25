import os
from pathlib import Path
from pydantic import BaseModel
from shared.config import AgentSettings, RagSettings, PathSettings, BaseConfig, load_yaml_config


class Settings(BaseModel):
    """Top-level configuration model"""
    agents: dict[str, AgentSettings]
    rag: RagSettings
    paths: PathSettings


class Config(BaseConfig):
    def __init__(self):
        super().__init__(Path(__file__).parent, Settings)

    @property
    def cv_analyst_model(self) -> str:
        return self._get_agent_setting("cv_analyst", "model")

    @property
    def cv_analyst_temperature(self) -> str:
        return str(self._get_agent_setting("cv_analyst", "temperature"))

    @property
    def job_analyst_model(self) -> str:
        return self._get_agent_setting("job_analyst", "model")

    @property
    def job_analyst_temperature(self) -> str:
        return str(self._get_agent_setting("job_analyst", "temperature"))

    @property
    def cv_strategist_model(self) -> str:
        return self._get_agent_setting("cv_strategist", "model")

    @property
    def cv_strategist_temperature(self) -> str:
        return str(self._get_agent_setting("cv_strategist", "temperature"))

    @property
    def cv_rewriter_model(self) -> str:
        return self._get_agent_setting("cv_rewriter", "model")

    @property
    def cv_rewriter_temperature(self) -> str:
        return str(self._get_agent_setting("cv_rewriter", "temperature"))

    @property
    def crew_manager_model(self) -> str:
        return self._get_agent_setting("crew_manager", "model")

    @property
    def crew_manager_temperature(self) -> str:
        return str(self._get_agent_setting("crew_manager", "temperature"))

    @property
    def knowledge_base_abspath(self) -> str:
        return os.path.abspath(self._settings.paths.knowledge_base)

    @property
    def vector_db_abspath(self) -> str:
        return os.path.abspath(self._settings.paths.vector_db)


def get_config() -> Config:
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
