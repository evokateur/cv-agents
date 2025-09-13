from crewai import Task
from optimizer.models import JobPosting, CvTransformationPlan, CurriculumVitae
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

    def cv_alignment_task(self, agent, context_tasks) -> Task:
        return Task(
            config=self.tasks_config["cv_alignment_task"],
            output_pydantic=CvTransformationPlan,
            context=context_tasks,
            agent=agent,
        )

    def cv_optimization_task(self, agent, context_tasks) -> Task:
        return Task(
            config=self.tasks_config["cv_optimization_task"],
            output_pydantic=CurriculumVitae,
            context=context_tasks,
            agent=agent,
        )
