import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

    @property
    def job_analyst_model(self) -> str:
        model = os.getenv("JOB_ANALYST_MODEL")
        assert model is not None, "JOB_ANALYST_MODEL environment variable must be set"
        return model

    @property
    def job_analyst_temperature(self) -> str:
        return os.getenv("JOB_ANALYST_TEMPERATURE", "0.7")

    @property
    def candidate_profiler_model(self) -> str:
        model = os.getenv("CANDIDATE_PROFILER_MODEL")
        assert model is not None, (
            "CANDIDATE_PROFILER_MODEL environment variable must be set"
        )
        return model

    @property
    def candidate_profiler_temperature(self) -> str:
        return os.getenv("CANDIDATE_PROFILER_TEMPERATURE", "0.7")

    @property
    def cv_strategist_model(self) -> str:
        model = os.getenv("CV_STRATEGIST_MODEL")
        assert model is not None, "CV_STRATEGIST_MODEL environment variable must be set"
        return model

    @property
    def cv_strategist_temperature(self) -> str:
        return os.getenv("CV_STRATEGIST_TEMPERATURE", "0.7")

    @property
    def crew_manager_model(self) -> str:
        model = os.getenv("CREW_MANAGER_MODEL")
        assert model is not None, "CREW_MANAGER_MODEL environment variable must be set"
        return model

    @property
    def crew_manager_temperature(self) -> str:
        return os.getenv("CREW_MANAGER_TEMPERATURE", "0.7")


def get_config() -> Config:
    return Config()
