from crewai import Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from optimizer.agents import CustomAgents
from optimizer.tasks import CustomTasks
from optimizer.fakers import FakeAgents, FakeTasks
from typing import List


@CrewBase
class CvOptimizer:
    """CV Optimizer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    @agent
    def cv_structurer(self):
        return self.custom_agents.cv_structurer()

    @agent
    def job_analyst(self):
        return self.custom_agents.job_analyst()

    @agent
    def cv_advisor(self):
        return self.custom_agents.cv_advisor()

    @agent
    def cv_strategist(self):
        return self.custom_agents.cv_strategist()

    @task
    def cv_structuring_task(self):
        task = self.custom_tasks.cv_structuring_task(self.cv_structurer())
        task.async_execution = True
        return task

    @task
    def job_analysis_task(self):
        task = self.custom_tasks.job_analysis_task(self.job_analyst())
        task.async_execution = True
        return task

    @task
    def cv_alignment_task(self):
        return self.custom_tasks.cv_alignment_task(
            self.cv_advisor(), [self.cv_structuring_task(), self.job_analysis_task()]
        )

    @task
    def cv_optimization_task(self):
        return self.custom_tasks.cv_optimization_task(
            self.cv_strategist(),
            [
                self.cv_structuring_task(),
                self.job_analysis_task(),
                self.cv_alignment_task(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


class CvStructuring:
    """CV Structuring crew - runs only CV structuring task"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def crew(self) -> Crew:
        cv_structurer = self.custom_agents.cv_structurer()
        cv_structuring_task = self.custom_tasks.cv_structuring_task(cv_structurer)

        return Crew(
            agents=[cv_structurer],
            tasks=[cv_structuring_task],
            process=Process.sequential,
            verbose=True,
        )


class JobAnalysis:
    """Job Analysis crew - runs only job analysis task"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def crew(self) -> Crew:
        job_analyst = self.custom_agents.job_analyst()
        job_analysis_task = self.custom_tasks.job_analysis_task(job_analyst)

        return Crew(
            agents=[job_analyst],
            tasks=[job_analysis_task],
            process=Process.sequential,
            verbose=True,
        )


class CvAlignment:
    """CV Alignment crew - runs only cv alignment task"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def crew(self) -> Crew:
        fake_cv_structurer = FakeAgents.cv_structurer()
        fake_job_analyst = FakeAgents.job_analyst()
        cv_advisor = self.custom_agents.cv_advisor()

        fake_cv_structuring_task = FakeTasks.cv_structuring_task(fake_cv_structurer)
        fake_cv_structuring_task.async_execution = True

        fake_job_analysis_task = FakeTasks.job_analysis_task(fake_job_analyst)
        fake_job_analysis_task.async_execution = True

        cv_alignment_task = self.custom_tasks.cv_alignment_task(
            cv_advisor, [fake_cv_structuring_task, fake_job_analysis_task]
        )

        return Crew(
            agents=[fake_cv_structurer, fake_job_analyst, cv_advisor],
            tasks=[fake_cv_structuring_task, fake_job_analysis_task, cv_alignment_task],
            process=Process.sequential,
            verbose=True,
        )


class CvOptimization:
    """CV Optimization crew - runs only cv optimization task using pre-generated files"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def crew(self) -> Crew:
        fake_cv_structurer = FakeAgents.cv_structurer()
        fake_job_analyst = FakeAgents.job_analyst()
        fake_cv_advisor = FakeAgents.cv_advisor()
        cv_strategist = self.custom_agents.cv_strategist()

        fake_cv_structuring_task = FakeTasks.cv_structuring_task(fake_cv_structurer)
        fake_cv_structuring_task.async_execution = True

        fake_job_analysis_task = FakeTasks.job_analysis_task(fake_job_analyst)
        fake_job_analysis_task.async_execution = True

        fake_cv_alignment_task = FakeTasks.cv_alignment_task(fake_cv_advisor)
        fake_cv_alignment_task.context = [
            fake_cv_structuring_task,
            fake_job_analysis_task,
        ]

        cv_optimization_task = self.custom_tasks.cv_optimization_task(
            cv_strategist,
            [fake_cv_structuring_task, fake_job_analysis_task, fake_cv_alignment_task],
        )

        return Crew(
            agents=[
                fake_cv_structurer,
                fake_job_analyst,
                fake_cv_advisor,
                cv_strategist,
            ],
            tasks=[
                fake_cv_structuring_task,
                fake_job_analysis_task,
                fake_cv_alignment_task,
                cv_optimization_task,
            ],
            process=Process.sequential,
            verbose=True,
        )
