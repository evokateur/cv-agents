from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, RagTool
from config import get_config
import yaml
import os


class CustomAgents:
    def __init__(self):
        # Load configs
        with open("optimizer_new/config/agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)

        # Initialize LLMs
        config = get_config()
        self.llms = {
            "job_analyst": LLM(
                model=config.job_analyst_model,
                temperature=float(config.job_analyst_temperature),
            ),
            "candidate_profiler": LLM(
                model=config.candidate_profiler_model,
                temperature=float(config.candidate_profiler_temperature),
            ),
            "cv_strategist": LLM(
                model=config.cv_strategist_model,
                temperature=float(config.cv_strategist_temperature),
            ),
        }

    def knowledge_base_rag_tool(self) -> RagTool:
        config = get_config()
        vector_db_path = os.path.abspath("vector_db")

        rag_tool = RagTool(
            config=dict(
                llm=dict(
                    provider="openai",
                    config=dict(
                        model=config.candidate_profiler_model,
                        temperature=float(config.candidate_profiler_temperature),
                    ),
                ),
                embedder=dict(
                    provider="openai",
                    config=dict(
                        model="text-embedding-ada-002",
                    ),
                ),
                chunker=dict(
                    chunk_size=1000,
                    chunk_overlap=200,
                ),
                vectordb=dict(
                    provider="chroma",
                    config=dict(
                        dir=vector_db_path,
                        collection_name="knowledge_base",
                        allow_reset=True,
                    ),
                ),
            )
        )

        if not os.path.exists(vector_db_path):
            knowledge_base_path = os.path.abspath("knowledge-base")

            if not os.path.exists(knowledge_base_path):
                raise FileNotFoundError(
                    f"Knowledge base directory not found: {knowledge_base_path}"
                )

            rag_tool.add(knowledge_base_path, data_type="directory")

        return rag_tool

    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llms["job_analyst"],
        )

    def candidate_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["candidate_profiler"],
            tools=[self.knowledge_base_rag_tool(), FileReadTool()],
            llm=self.llms["candidate_profiler"],
        )

    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_strategist"],
            tools=[FileReadTool()],
            llm=self.llms["cv_strategist"],
        )
