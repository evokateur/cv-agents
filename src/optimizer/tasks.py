from crewai import Task
from optimizer.models import CvTransformationPlan
from models.schema import JobPosting, CurriculumVitae
from optimizer.utils.prompt_utils import render_pydantic_models_in_prompt
import yaml


class CustomTasks:
    def __init__(self):
        import os
        config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")
        with open(config_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)

    def cv_analysis_task(self, agent) -> Task:
        return Task(
            config=self.tasks_config["cv_analysis_task"],
            output_pydantic=CurriculumVitae,
            agent=agent,
        )

    def job_analysis_task(self, agent) -> Task:
        return Task(
            config=self.tasks_config["job_analysis_task"],
            output_pydantic=JobPosting,
            agent=agent,
        )

    def cv_alignment_task(self, agent, context_tasks) -> Task:
        # Inject schema into the task description
        task_config = self.tasks_config["cv_alignment_task"].copy()
        model_registry = {"CurriculumVitae": CurriculumVitae}
        task_config["description"] = render_pydantic_models_in_prompt(
            task_config["description"], model_registry
        )

        return Task(
            config=task_config,
            output_pydantic=CvTransformationPlan,
            context=context_tasks,
            agent=agent,
        )

    def cv_transformation_task(self, agent, context_tasks) -> Task:
        return Task(
            config=self.tasks_config["cv_transformation_task"],
            output_pydantic=CurriculumVitae,
            context=context_tasks,
            agent=agent,
        )
