from crewai import Agent


job_analyst = Agent(
    role="Job Requirements Analyst",
    goal="Extract and structure job posting requirements from URLs or text",
    backstory="Expert at parsing job postings and identifying key requirements, skills, and qualifications",
    tools=[],  # Will be populated when tools are implemented
    verbose=True
)