import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
import yaml


class AgentSettings(BaseModel):
    """Configuration for a single agent"""
    model: str = Field(min_length=1, description="LLM model name")
    temperature: float = Field(ge=0.0, le=2.0, description="LLM temperature (0.0-2.0)")


class RagSettings(BaseModel):
    """Configuration for RAG (Retrieval-Augmented Generation)"""
    embedding_model: str = Field(min_length=1)
    collection_name: str = Field(min_length=1)
    num_results: int = Field(gt=0, description="Number of results to retrieve")
    chunk_size: int = Field(ge=100, description="Chunk size for text splitting")
    chunk_overlap: int = Field(ge=0, description="Overlap between chunks")

    @field_validator('chunk_overlap')
    @classmethod
    def overlap_less_than_size(cls, v, info):
        if 'chunk_size' in info.data and v >= info.data['chunk_size']:
            raise ValueError('chunk_overlap must be less than chunk_size')
        return v


class PathSettings(BaseModel):
    """Configuration for file paths"""
    knowledge_base: str
    vector_db: str


class Settings(BaseModel):
    """Top-level configuration model"""
    agents: dict[str, AgentSettings]
    rag: RagSettings
    paths: PathSettings


def _load_yaml_config() -> dict:
    """Load settings from YAML files with override hierarchy:
    settings.yaml -> settings.local.yaml

    YAML files are the single source of truth for configuration.
    Environment variables are only used for API keys (secrets).
    """
    config_dir = Path(__file__).parent
    settings_file = config_dir / "settings.yaml"
    local_settings_file = config_dir / "settings.local.yaml"

    # Load base settings
    if not settings_file.exists():
        raise FileNotFoundError(f"Required settings file not found: {settings_file}")

    with open(settings_file) as f:
        config = yaml.safe_load(f) or {}

    # Override with local settings if present
    if local_settings_file.exists():
        with open(local_settings_file) as f:
            local_config = yaml.safe_load(f) or {}
            _deep_merge(config, local_config)

    return config


def _deep_merge(base: dict, override: dict) -> None:
    """Recursively merge override dict into base dict"""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


class Config:
    def __init__(self):
        load_dotenv()
        yaml_config = _load_yaml_config()
        # Validate with Pydantic - will raise ValidationError if invalid
        self._settings = Settings(**yaml_config)

    def _get_agent_setting(self, agent_name: str, setting: str):
        """Get agent setting from validated Pydantic model"""
        agent = self._settings.agents.get(agent_name)
        if agent is None:
            raise ValueError(f"Agent '{agent_name}' not found in settings.yaml")
        return getattr(agent, setting)

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
    yaml_config = _load_yaml_config()
    settings = Settings(**yaml_config)

    return {
        "embedding_model": settings.rag.embedding_model,
        "collection_name": settings.rag.collection_name,
        "num_results": settings.rag.num_results,
        "chunk_size": settings.rag.chunk_size,
        "chunk_overlap": settings.rag.chunk_overlap,
    }
