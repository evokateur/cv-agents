from crewai import Task
from optimizer.models import CurriculumVitae
from optimizer.agents.cv_strategist import cv_strategist


def create_cv_strategizing_task(
    job_analysis_task: Task, candidate_profiling_task: Task
) -> Task:
    return Task(
        description=(
            "Using the job requirements and candidate profile, create an optimized CV by:\n"
            "- Prioritizing experiences that best match job requirements\n"
            "- Rewriting descriptions to emphasize relevant skills and achievements\n"
            "- Optimizing keyword density for ATS compatibility\n"
            "- Structuring sections to highlight strengths for this specific role\n"
            "- Quantifying achievements and impact where possible\n"
            "- Ensuring language matches the job posting's tone and terminology"
        ),
        expected_output=(
            "An OptimizedCV object with restructured and rewritten content sections "
            "tailored specifically to the job requirements, optimized for both ATS "
            "and human review."
        ),
        output_pydantic=CurriculumVitae,
        context=[
            job_analysis_task,
            candidate_profiling_task,
        ],
        agent=cv_strategist,
    )
