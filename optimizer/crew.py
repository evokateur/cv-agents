from crewai import Crew, Process, Task, Agent
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from optimizer.agents import CustomAgents
from optimizer.tasks import CustomTasks
from optimizer.models import JobPosting
from typing import List
import json


@CrewBase
class CvOptimizer:
    """CV Optimizer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    @agent
    def job_analyst(self):
        return self.custom_agents.job_analyst()

    @agent
    def candidate_profiler(self):
        return self.custom_agents.candidate_profiler()

    @agent
    def cv_strategist(self):
        return self.custom_agents.cv_strategist()

    @task
    def job_analysis_task(self):
        return self.custom_tasks.job_analysis_task(self.job_analyst())

    @task
    def candidate_profiling_task(self):
        return self.custom_tasks.candidate_profiling_task(
            self.candidate_profiler(), [self.job_analysis_task()]
        )

    @task
    def cv_optimization_task(self):
        return self.custom_tasks.cv_optimization_task(
            self.cv_strategist(),
            [self.job_analysis_task(), self.candidate_profiling_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


class JobAnalysisTest:
    """Job Analysis Test crew - runs only job analysis task"""

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


class CandidateProfilingTest:
    """Candidate Profiling Test crew - runs only candidate profiling task"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def _fake_job_analyst(self) -> Agent:
        """Fake agent that loads job analysis output from file"""
        return Agent(
            role="Job Analysis File Reader",
            goal="Load job analysis output from file and pass it to candidate profiler",
            backstory="A utility agent that reads pre-generated job analysis files",
            verbose=True,
        )

    def _fake_job_analysis_task(self, agent) -> Task:
        """Fake task that loads job analysis output from file"""
        return Task(
            description="Load job analysis output from {output_directory}/job_analysis.json and return it as structured data",
            expected_output="JobPosting object loaded from the job analysis output file",
            agent=agent,
            output_pydantic=JobPosting,
        )

    def crew(self) -> Crew:
        fake_job_analyst = self._fake_job_analyst()
        candidate_profiler = self.custom_agents.candidate_profiler()
        
        fake_job_analysis_task = self._fake_job_analysis_task(fake_job_analyst)
        candidate_profiling_task = self.custom_tasks.candidate_profiling_task(candidate_profiler, [fake_job_analysis_task])
        
        return Crew(
            agents=[fake_job_analyst, candidate_profiler],
            tasks=[fake_job_analysis_task, candidate_profiling_task],
            process=Process.sequential,
            verbose=True,
        )
