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


def get_config() -> Config:
    return Config()
