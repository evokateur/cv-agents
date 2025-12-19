from crewai import Agent, LLM
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    FileReadTool,
    DirectorySearchTool,
)
from optimizer.config.settings import get_config
from optimizer.tools.knowledge_base_tool import KnowledgeBaseTool
import yaml


class CustomAgents:
    def __init__(self):
        # Load configs
        import os
        config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
        with open(config_path, "r") as f:
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
            "cv_strategist": LLM(
                model=self.config.cv_strategist_model,
                temperature=float(self.config.cv_strategist_temperature),
            ),
            "cv_rewriter": LLM(
                model=self.config.cv_rewriter_model,
                temperature=float(self.config.cv_rewriter_temperature),
            ),
        }

        # Import here to avoid circular dependency
        from shared.embedder import KnowledgeBaseEmbedder
        self.embedder = KnowledgeBaseEmbedder(
            knowledge_base_abspath=self.config.knowledge_base_abspath,
            vector_db_abspath=self.config.vector_db_abspath,
            force_rebuild=False,
        )

    def get_knowledge_base_tool(self) -> KnowledgeBaseTool:
        return KnowledgeBaseTool(vector_db_path=self.config.vector_db_abspath)

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

    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_strategist"],
            tools=[
                self.get_knowledge_base_tool(),
                FileReadTool(),
            ],
            llm=self.llms["cv_strategist"],
        )

    def cv_rewriter(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_rewriter"],
            tools=[
                self.get_knowledge_base_tool(),
                self.get_directory_search_tool(),
                self.get_file_read_tool(),
            ],
            llm=self.llms["cv_rewriter"],
        )
