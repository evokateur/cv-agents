from pathlib import Path
from pydantic import BaseModel
from shared.config import AgentSettings, BaseConfig, load_yaml_config
from config.settings import get_config as get_shared_config


class Settings(BaseModel):
    """Optimizer-specific configuration model (agents only)"""
    agents: dict[str, AgentSettings]


class Config(BaseConfig):
    def __init__(self):
        super().__init__(Path(__file__).parent, Settings)
        # Import shared config for paths
        self._shared_config = get_shared_config()

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
        return self._shared_config.knowledge_base_abspath

    @property
    def vector_db_abspath(self) -> str:
        return self._shared_config.vector_db_abspath


def get_config() -> Config:
    """Get optimizer configuration (includes shared config via delegation)"""
    return Config()
