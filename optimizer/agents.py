from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, RagTool
from config import get_config
from optimizer.vector_builder import VectorDbBuilder
from optimizer.utils.vector_utils import is_valid_chroma_vector_db
import yaml


class CustomAgents:
    def __init__(self):
        # Load configs
        with open("optimizer/config/agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)

        # Initialize LLMs
        self.config = get_config()
        self.llms = {
            "job_analyst": LLM(
                model=self.config.job_analyst_model,
                temperature=float(self.config.job_analyst_temperature),
            ),
            "candidate_profiler": LLM(
                model=self.config.candidate_profiler_model,
                temperature=float(self.config.candidate_profiler_temperature),
            ),
            "cv_strategist": LLM(
                model=self.config.cv_strategist_model,
                temperature=float(self.config.cv_strategist_temperature),
            ),
        }

    def get_rag_tool(self) -> RagTool:
        builder = VectorDbBuilder(
            knowledge_base_abspath=self.config.knowledge_base_abspath,
            vector_db_abspath=self.config.vector_db_abspath,
            force_rebuild=False,
        )

        builder.build_if_needed()

        if not is_valid_chroma_vector_db(self.config.vector_db_abspath):
            raise ValueError(
                "Invalid Chroma vector DB path: {}".format(
                    self.config.vector_db_abspath
                )
            )

        return RagTool(
            name="CandidateKnowledgeBase",
            config={
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": self.config.candidate_profiler_model,
                    },
                },
                "vectordb": {
                    "provider": "chroma",
                    "config": {"dir": self.config.vector_db_abspath},
                },
            },
        )

    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llms["job_analyst"],
        )

    def candidate_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["candidate_profiler"],
            tools=[self.get_rag_tool(), FileReadTool()],
            llm=self.llms["candidate_profiler"],
        )

    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_strategist"],
            tools=[FileReadTool()],
            llm=self.llms["cv_strategist"],
        )
