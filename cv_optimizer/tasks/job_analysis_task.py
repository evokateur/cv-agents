from crewai import Task
from cv_agents.models import JobPosting
from cv_agents.agents.job_analyst import job_analyst


def create_job_analysis_task(job_url: str) -> Task:
    return Task(
        description=(
            "Analyze the job posting URL provided ({job_posting_url}) to extract and structure "
            "the following information:\n"
            "- Job title and company name\n"
            "- Industry sector\n"
            "- Complete job description\n"
            "- Experience level required (entry, mid, senior, etc.)\n"
            "- General requirements (education, certifications, years of experience)\n"
            "- Required skills (must-have technical and soft skills)\n"
            "- Preferred skills (nice-to-have skills that give candidates an advantage)\n"
            "- Key responsibilities and day-to-day activities\n"
            "Use the scraping and search tools to gather comprehensive information."
        ),
        expected_output=(
            "A structured JobPosting object containing title, company, industry, "
            "description, experience_level, requirements, required_skills, "
            "preferred_skills, and responsibilities extracted from the job posting."
        ),
        output_pydantic=JobPosting,
        agent=job_analyst,
        async_execution=True,
    )
