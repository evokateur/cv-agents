from crewai import Crew
from optimizer.tasks.job_analysis_task import create_job_analysis_task
from optimizer.models import JobPosting
from optimizer.agents.job_analyst import job_analyst


def test_job_analysis_task_with_real_url():
    task = create_job_analysis_task(job_analyst)

    crew = Crew(agents=[job_analyst], tasks=[task])

    inputs = {
        "job_posting_url": "https://automattic.com/work-with-us/job/experienced-software-engineer/"
    }

    result = crew.kickoff(inputs)

    job_posting = JobPosting.model_validate(result.pydantic)

    # Assert job title is not empty
    assert job_posting.title == "Experienced Software Engineer"
