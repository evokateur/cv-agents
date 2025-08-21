from crewai import Agent, Task
from optimizer.models import JobPosting


def create_job_analysis_task(analyst: Agent) -> Task:
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
        output_file="{output_directory}/job_analysis.json",
        agent=analyst,
    )
