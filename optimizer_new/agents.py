from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool
from optimizer_new.tools import knowledge_base_rag_tool
from config import get_config
import yaml


class AgentFactory:
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

    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llms["job_analyst"],
        )

    def candidate_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["candidate_profiler"],
            tools=[knowledge_base_rag_tool, FileReadTool()],
            llm=self.llms["candidate_profiler"],
        )

    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_strategist"],
            tools=[FileReadTool()],
            llm=self.llms["cv_strategist"],
        )
