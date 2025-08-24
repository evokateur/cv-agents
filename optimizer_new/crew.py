from crewai import Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from optimizer_new.agents import AgentFactory
from optimizer_new.tasks import TaskFactory
from typing import List


@CrewBase
class CvOptimizer:
    """CV Optimizer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.agent_factory = AgentFactory()
        self.task_factory = TaskFactory()

    @agent
    def job_analyst(self):
        return self.agent_factory.job_analyst()

    @agent
    def candidate_profiler(self):
        return self.agent_factory.candidate_profiler()

    @agent
    def cv_strategist(self):
        return self.agent_factory.cv_strategist()

    @task
    def job_analysis_task(self):
        return self.task_factory.job_analysis_task(self.job_analyst())

    @task
    def candidate_profiling_task(self):
        return self.task_factory.candidate_profiling_task(
            self.candidate_profiler(), [self.job_analysis_task()]
        )

    @task
    def cv_optimization_task(self):
        return self.task_factory.cv_optimization_task(
            self.cv_strategist(), [self.job_analysis_task(), self.candidate_profiling_task()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

