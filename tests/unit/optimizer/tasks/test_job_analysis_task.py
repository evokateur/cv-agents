from crewai import Crew
from langchain_openai import ChatOpenAI
from optimizer.tasks.job_analysis_task import create_job_analysis_task
from optimizer.models import JobPosting
from optimizer.agents.job_analyst import job_analyst


def test_job_analysis_task_with_real_url():
    job_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"

    task = create_job_analysis_task(job_url)
    crew = Crew(agents=[job_analyst], tasks=[task])

    result = crew.kickoff(inputs={"job_posting_url": job_url})

    job_posting = result.pydantic

    # Assert job title is not empty
    assert job_posting.title
