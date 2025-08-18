from crewai import Agent, Task
from optimizer.models import CandidateProfile


def create_candidate_profiling_task(profiler: Agent, job_analysis: Task) -> Task:
    return Task(
        description=(
            "Using the job requirements from the job analysis, search the knowledge base "
            "to build a comprehensive candidate profile. Focus on:\n"
            "- Projects and experiences that match required and preferred skills\n"
            "- Relevant technical achievements and business impact\n"
            "- Leadership and collaboration examples that fit the role level\n"
            "- Domain expertise that aligns with the industry and responsibilities\n"
            "- Quantifiable results and outcomes from past work\n"
            "Use semantic search to find related experiences even if not exact keyword matches."
        ),
        expected_output=(
            "A structured CandidateProfile containing relevant experiences, matching skills, "
            "key projects, achievements, and contextual information tailored to the job requirements."
        ),
        output_pydantic=CandidateProfile,
        context=[job_analysis],
        agent=profiler,
    )
