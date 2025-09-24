from crewai import Agent, LLM
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    FileReadTool,
    DirectorySearchTool,
)
from config import get_config, get_embedchain_config
from optimizer.tools.semantic_search_tool import SemanticSearchTool
from optimizer.tools.semantic_search_wrapper import SemanticSearchWrapper
from optimizer.knowledge_embedder import KnowledgeBaseEmbedder
import yaml


class CustomAgents:
    def __init__(self):
        # Load configs
        with open("optimizer/config/agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)

        # Initialize LLMs
        self.config = get_config()
        self.llms = {
            "cv_analyst": LLM(
                model=self.config.cv_analyst_model,
                temperature=float(self.config.cv_analyst_temperature),
            ),
            "job_analyst": LLM(
                model=self.config.job_analyst_model,
                temperature=float(self.config.job_analyst_temperature),
            ),
            "cv_advisor": LLM(
                model=self.config.cv_advisor_model,
                temperature=float(self.config.cv_advisor_temperature),
            ),
            "cv_strategist": LLM(
                model=self.config.cv_strategist_model,
                temperature=float(self.config.cv_strategist_temperature),
            ),
        }

        self.embedder = KnowledgeBaseEmbedder(
            knowledge_base_abspath=self.config.knowledge_base_abspath,
            vector_db_abspath=self.config.vector_db_abspath,
            force_rebuild=False,
        )

    def get_semantic_search_tool(self) -> SemanticSearchWrapper:
        return SemanticSearchWrapper(config=get_embedchain_config())

    def get_directory_search_tool(self) -> DirectorySearchTool:
        return DirectorySearchTool(
            directory_path=self.config.knowledge_base_abspath,
            recursive=True,
        )

    def get_file_read_tool(self) -> FileReadTool:
        return FileReadTool()

    def cv_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_analyst"],
            tools=[FileReadTool()],
            llm=self.llms["cv_analyst"],
        )

    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llms["job_analyst"],
        )

    def cv_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_advisor"],
            tools=[
                self.get_semantic_search_tool(),
                self.get_directory_search_tool(),
                FileReadTool(),
            ],
            llm=self.llms["cv_advisor"],
        )

    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_strategist"],
            tools=[
                self.get_semantic_search_tool(),
                self.get_directory_search_tool(),
                self.get_file_read_tool(),
            ],
            llm=self.llms["cv_strategist"],
        )
