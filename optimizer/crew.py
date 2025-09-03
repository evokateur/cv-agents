from crewai import Crew, Process, Task, Agent
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from optimizer.agents import CustomAgents
from optimizer.tasks import CustomTasks
from optimizer.models import JobPosting
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
    def job_analyst(self):
        return self.custom_agents.job_analyst()

    @agent
    def cv_advisor(self):
        return self.custom_agents.cv_advisor()

    @agent
    def cv_strategist(self):
        return self.custom_agents.cv_strategist()

    @task
    def job_analysis_task(self):
        return self.custom_tasks.job_analysis_task(self.job_analyst())

    @task
    def cv_alignment_task(self):
        return self.custom_tasks.cv_alignment_task(
            self.cv_advisor(), [self.job_analysis_task()]
        )

    @task
    def cv_optimization_task(self):
        return self.custom_tasks.cv_optimization_task(
            self.cv_strategist(),
            [self.job_analysis_task(), self.cv_alignment_task()],
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


class CvAlignmentTest:
    """CV Alignment Test crew - runs only cv alignment task"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def _fake_job_analyst(self) -> Agent:
        """Fake agent that loads job analysis output from file"""
        from crewai_tools import FileReadTool
        return Agent(
            role="Job Analysis File Reader",
            goal="Load job analysis output from file and pass it to cv advisor",
            backstory="A utility agent that reads pre-generated job analysis files",
            tools=[FileReadTool()],
            verbose=True,
        )

    def _fake_job_analysis_task(self, agent) -> Task:
        """Fake task that loads job analysis output from file"""
        return Task(
            description="""
            Use the FileReadTool to read the job analysis JSON file at {output_directory}/job_analysis.json.
            Parse the JSON content and extract the exact job details including:
            - title (company name)
            - company (exact company name) 
            - technical_skills, hard_requirements, preferred_skills
            - responsibilities and keywords
            
            Return this data as a structured JobPosting object with the EXACT values from the file.
            Do not modify, interpret, or make up any job details.
            """,
            expected_output="JobPosting object with exact data from the job_analysis.json file",
            agent=agent,
            output_pydantic=JobPosting,
        )

    def crew(self) -> Crew:
        fake_job_analyst = self._fake_job_analyst()
        cv_advisor = self.custom_agents.cv_advisor()

        fake_job_analysis_task = self._fake_job_analysis_task(fake_job_analyst)
        cv_alignment_task = self.custom_tasks.cv_alignment_task(
            cv_advisor, [fake_job_analysis_task]
        )

        return Crew(
            agents=[fake_job_analyst, cv_advisor],
            tasks=[fake_job_analysis_task, cv_alignment_task],
            process=Process.sequential,
            verbose=True,
        )
