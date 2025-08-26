from crewai import Task
from optimizer.models import JobPosting, CandidateProfile, CurriculumVitae
from optimizer.utils.prompt_utils import render_pydantic_models_in_prompt
import yaml


class CustomTasks:
    def __init__(self):
        with open("optimizer/config/tasks.yaml", "r") as f:
            self.tasks_config = yaml.safe_load(f)

    def job_analysis_task(self, agent) -> Task:
        return Task(
            config=self.tasks_config["job_analysis_task"],
            output_pydantic=JobPosting,
            agent=agent,
        )

    def candidate_profiling_task(self, agent, context_tasks) -> Task:
        description_template = """
        You will receive structured job requirements from the job analysis task:

        [[JobPosting]]

        Your task is to build a comprehensive candidate profile by searching the CandidateKnowledgeBase
        and synthesizing relevant information. When constructing the profile, focus on:

        - Projects and experiences that match required and preferred skills
        - Relevant technical achievements and their business impact
        - Leadership and collaboration examples appropriate to the role level
        - Domain expertise aligned with the industry and responsibilities
        - Quantifiable results and measurable outcomes from past work

        Use semantic search to find related experiences, even if the match is not exact. 
        Summarize and integrate these findings into a structured CandidateProfile object 
        tailored to the provided job requirements.
        """

        rendered_description = render_pydantic_models_in_prompt(
            description_template, model_registry={"JobPosting": JobPosting}
        )

        return Task(
            config=self.tasks_config["candidate_profiling_task"],
            description=rendered_description,
            output_pydantic=CandidateProfile,
            context=context_tasks,
            agent=agent,
        )

    def cv_optimization_task(self, agent, context_tasks) -> Task:
        description_template = """
        You will receive three inputs to complete this task:

        1. A structured job posting object with the following fields:
        [[JobPosting]]

        2. A structured candidate profile object with the following fields:
        [[CandidateProfile]]

        3. A file path to the candidate's existing CV:
        {cv_data_path}

        Your task is to optimize the candidate’s CV for the target job by:
        - Prioritizing experiences that best match the required and preferred skills
        - Rewriting descriptions to emphasize relevant achievements and responsibilities
        - Optimizing keyword usage for applicant tracking system (ATS) compatibility
        - Structuring sections to highlight strengths for this specific role
        - Quantifying impact (e.g., metrics, results) wherever possible
        - Aligning language, tone, and terminology with the job posting

        Your final output must be a structured CurriculumVitae object that is tailored to the job requirements and enriched with the candidate’s strongest qualifications.
        """
        rendered_description = render_pydantic_models_in_prompt(
            description_template,
            model_registry={
                "JobPosting": JobPosting,
                "CandidateProfile": CandidateProfile,
            },
        )

        return Task(
            config=self.tasks_config["cv_optimization_task"],
            description=rendered_description,
            output_pydantic=CurriculumVitae,
            context=context_tasks,
            agent=agent,
        )
