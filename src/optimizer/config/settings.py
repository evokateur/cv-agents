import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

    @property
    def cv_analyst_model(self) -> str:
        model = os.getenv("CV_ANALYST_MODEL")
        assert model is not None, "CV_ANALYST_MODEL environment variable must be set"
        return model

    @property
    def cv_analyst_temperature(self) -> str:
        return os.getenv("CV_ANALYST_TEMPERATURE", "0.7")

    @property
    def job_analyst_model(self) -> str:
        model = os.getenv("JOB_ANALYST_MODEL")
        assert model is not None, "JOB_ANALYST_MODEL environment variable must be set"
        return model

    @property
    def job_analyst_temperature(self) -> str:
        return os.getenv("JOB_ANALYST_TEMPERATURE", "0.7")

    @property
    def cv_strategist_model(self) -> str:
        model = os.getenv("CV_STRATEGIST_MODEL")
        assert model is not None, (
            "CV_STRATEGIST_MODEL environment variable must be set"
        )
        return model

    @property
    def cv_strategist_temperature(self) -> str:
        return os.getenv("CV_STRATEGIST_TEMPERATURE", "0.7")

    @property
    def cv_rewriter_model(self) -> str:
        model = os.getenv("CV_REWRITER_MODEL")
        assert model is not None, "CV_REWRITER_MODEL environment variable must be set"
        return model

    @property
    def cv_rewriter_temperature(self) -> str:
        return os.getenv("CV_REWRITER_TEMPERATURE", "0.7")

    @property
    def crew_manager_model(self) -> str:
        model = os.getenv("CREW_MANAGER_MODEL")
        assert model is not None, "CREW_MANAGER_MODEL environment variable must be set"
        return model

    @property
    def crew_manager_temperature(self) -> str:
        return os.getenv("CREW_MANAGER_TEMPERATURE", "0.7")

    @property
    def knowledge_base_abspath(self) -> str:
        path = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge-base")
        return os.path.abspath(path)

    @property
    def vector_db_abspath(self) -> str:
        path = os.getenv("VECTOR_DB_PATH", "vector_db")
        return os.path.abspath(path)


def get_config() -> Config:
    return Config()


def get_rag_config() -> dict:
    return {
        "embedding_model": os.getenv("RAG_EMBEDDING_MODEL", "text-embedding-ada-002"),
        "collection_name": os.getenv("RAG_COLLECTION_NAME", "knowledge_base"),
        "num_results": int(os.getenv("RAG_NUM_RESULTS", "7")),
        "chunk_size": int(os.getenv("RAG_CHUNK_SIZE", "1000")),
        "chunk_overlap": int(os.getenv("RAG_CHUNK_OVERLAP", "200")),
    }
