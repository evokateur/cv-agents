import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


def create_llm() -> LLM:
    return LLM(
        model=os.getenv("JOB_ANALYST_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("JOB_ANALYST_TEMPERATURE", "0.7")),
    )


llm = create_llm()

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
