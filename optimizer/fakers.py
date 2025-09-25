from crewai import Agent, Task
from crewai_tools import FileReadTool
from optimizer.models import JobPosting, CurriculumVitae, CvTransformationPlan


class FakeAgents:
    """Utility agents that load pre-generated outputs from files"""

    @staticmethod
    def cv_analyst() -> Agent:
        """Fake agent that loads CV analysis output from file"""
        return Agent(
            role="CV Analysis File Reader",
            goal="Load CV analysis output from file",
            backstory="A utility agent that reads pre-generated CV analysis files",
            tools=[FileReadTool()],
            verbose=True,
        )

    @staticmethod
    def job_analyst() -> Agent:
        """Fake agent that loads job analysis output from file"""
        return Agent(
            role="Job Analysis File Reader",
            goal="Load job analysis output from file",
            backstory="A utility agent that reads pre-generated job analysis files",
            tools=[FileReadTool()],
            verbose=True,
        )

    @staticmethod
    def cv_strategist() -> Agent:
        """Fake agent that loads cv transformation plan from file"""
        return Agent(
            role="CV Transformation Plan Reader",
            goal="Load CV transformation plan from file",
            backstory="A utility agent that reads pre-generated CV transformation plan files",
            tools=[FileReadTool()],
            verbose=True,
        )


class FakeTasks:
    """Utility tasks that load pre-generated outputs from files"""

    @staticmethod
    def cv_analysis_task(agent: Agent) -> Task:
        """Fake task that loads CV analysis output from file"""
        return Task(
            description="""
            Use the FileReadTool to read the CV analysis JSON file at {output_directory}/original_cv.json.
            Parse the JSON content and extract the exact CV details including:
            - personal information, contact details
            - experience, education, skills sections
            - all structured data fields

            Return this data as a structured CurriculumVitae object with the EXACT values from the file.
            Do not modify, interpret, or make up any CV details.
            """,
            expected_output="CurriculumVitae object with exact data from the original_cv.json file",
            agent=agent,
            output_pydantic=CurriculumVitae,
        )

    @staticmethod
    def job_analysis_task(agent: Agent) -> Task:
        """Fake task that loads job analysis output from file"""
        return Task(
            description="""
            Use the FileReadTool to read the job analysis JSON file at {output_directory}/job_posting.json.
            Parse the JSON content and extract the exact job details including:
            - title (company name)
            - company (exact company name)
            - technical_skills, hard_requirements, preferred_skills
            - responsibilities and keywords

            Return this data as a structured JobPosting object with the EXACT values from the file.
            Do not modify, interpret, or make up any job details.
            """,
            expected_output="JobPosting object with exact data from the job_posting.json file",
            agent=agent,
            output_pydantic=JobPosting,
        )

    @staticmethod
    def cv_alignment_task(agent: Agent) -> Task:
        """Fake task that loads cv transformation plan from file"""
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