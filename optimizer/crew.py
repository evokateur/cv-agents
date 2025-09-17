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


class CvOptimization:
    """CV Optimization crew - runs only cv optimization task using pre-generated files"""

    def __init__(self):
        self.custom_agents = CustomAgents()
        self.custom_tasks = CustomTasks()

    def _fake_job_analyst(self) -> Agent:
        """Fake agent that loads job analysis output from file"""
        from crewai_tools import FileReadTool
        return Agent(
            role="Job Analysis File Reader",
            goal="Load job analysis output from file",
            backstory="A utility agent that reads pre-generated job analysis files",
            tools=[FileReadTool()],
            verbose=True,
        )

    def _fake_cv_advisor(self) -> Agent:
        """Fake agent that loads cv transformation plan from file"""
        from crewai_tools import FileReadTool
        return Agent(
            role="CV Transformation Plan Reader",
            goal="Load CV transformation plan from file",
            backstory="A utility agent that reads pre-generated CV transformation plan files",
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

    def _fake_cv_alignment_task(self, agent) -> Task:
        """Fake task that loads cv transformation plan from file"""
        from optimizer.models import CvTransformationPlan
        return Task(
            description="""
            Use the FileReadTool to read the CV transformation plan JSON file at {output_directory}/cv_transformation_plan.json.
            Parse the JSON content and extract the exact transformation plan including:
            - matching_skills, missing_skills
            - additions with file paths and quotes
            - rewrites with improved descriptions
            - transformation_strategy

            Return this data as a structured CvTransformationPlan object with the EXACT values from the file.
            Do not modify, interpret, or make up any transformation details.
            """,
            expected_output="CvTransformationPlan object with exact data from the cv_transformation_plan.json file",
            agent=agent,
            output_pydantic=CvTransformationPlan,
        )

    def crew(self) -> Crew:
        fake_job_analyst = self._fake_job_analyst()
        fake_cv_advisor = self._fake_cv_advisor()
        cv_strategist = self.custom_agents.cv_strategist()

        fake_job_analysis_task = self._fake_job_analysis_task(fake_job_analyst)
        fake_cv_alignment_task = self._fake_cv_alignment_task(fake_cv_advisor)
        cv_optimization_task = self.custom_tasks.cv_optimization_task(
            cv_strategist, [fake_job_analysis_task, fake_cv_alignment_task]
        )

        return Crew(
            agents=[fake_job_analyst, fake_cv_advisor, cv_strategist],
            tasks=[fake_job_analysis_task, fake_cv_alignment_task, cv_optimization_task],
            process=Process.sequential,
            verbose=True,
        )
