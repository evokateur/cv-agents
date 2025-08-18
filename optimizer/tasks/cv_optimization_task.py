from crewai import Agent, Task
from optimizer.models import CurriculumVitae


def create_cv_optimization_task(
    strategist: Agent, job_analysis: Task, candidate_profile: Task
) -> Task:
    return Task(
        description=(
            "Read the candidate's current cv data from {cv_data_path} and optimize it"
            "using the job requirements data and candidate profile. Create the optimized CV by:\n"
            "- Prioritizing experiences that best match job requirements\n"
            "- Rewriting descriptions to emphasize relevant skills and achievements\n"
            "- Optimizing keyword density for ATS compatibility\n"
            "- Structuring sections to highlight strengths for this specific role\n"
            "- Quantifying achievements and impact where possible\n"
            "- Ensuring language matches the job posting's tone and terminology"
        ),
        expected_output=(
            "A CurriculumVitae object with restructured and rewritten content sections "
            "tailored specifically to the job requirements, optimized for both ATS "
            "and human review."
        ),
        output_pydantic=CurriculumVitae,
        context=[
            job_analysis,
            candidate_profile,
        ],
        agent=strategist,
    )
