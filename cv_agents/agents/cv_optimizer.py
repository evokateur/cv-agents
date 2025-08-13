from crewai import Agent


cv_optimizer_agent = Agent(
    role="CV Optimizer",
    goal="Generate optimized CV data for specific job targeting",
    backstory="Specialist in tailoring CVs for maximum relevance while maintaining accuracy",
    tools=[],  # Will be populated when tools are implemented
    verbose=True
)