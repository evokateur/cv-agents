from crewai import Agent, Task
from optimizer.models import JobPosting, CandidateProfile


def create_file_loader_agent() -> Agent:
    return Agent(
        role="File Loader",
        goal="Load data from saved JSON files",
        backstory="A simple agent that reads previously saved task outputs from disk",
        verbose=False,
        allow_delegation=False,
    )


def create_fake_job_analysis_task(output_file_path: str, agent: Agent) -> Task:
    return Task(
        description=(
            f"Load job analysis results from the saved file: {output_file_path}. "
            "Read the JSON file and return it as a JobPosting object. "
            "This is a fake task used for debugging and testing purposes."
        ),
        expected_output=(
            "A JobPosting object loaded from the saved file, containing title, company, "
            "industry, description, experience_level, requirements, required_skills, "
            "preferred_skills, and responsibilities."
        ),
        output_pydantic=JobPosting,
        agent=agent,
    )


def create_fake_candidate_profiling_task(
    output_file_path: str, job_analysis: Task, agent: Agent
) -> Task:
    return Task(
        description=(
            f"Load candidate profile results from the saved file: {output_file_path}. "
            "Read the JSON file and return it as a CandidateProfile object. "
            "This is a fake task used for debugging and testing purposes."
        ),
        expected_output=(
            "A CandidateProfile object loaded from the saved file, containing relevant "
            "experiences, matching skills, key projects, achievements, and contextual "
            "information tailored to the job requirements."
        ),
        output_pydantic=CandidateProfile,
        context=[job_analysis],
        agent=agent,
    )
