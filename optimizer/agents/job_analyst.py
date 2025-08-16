from config import get_config
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

config = get_config()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

llm = LLM(
    model=config.job_analyst_model,
    temperature=float(config.job_analyst_temperature),
)

job_analyst = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on job posting to help job applicants",
    tools=[scrape_tool, search_tool],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Job Researcher, your prowess in navigating and extracting critical information from job postings is unmatched..."
    ),
)
