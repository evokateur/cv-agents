from crewai import Agent


fit_assessor = Agent(
    role="Compatibility Assessor",
    goal="Evaluate fit between background and job requirements",
    backstory="Expert at analyzing skill gaps, strengths, and overall compatibility",
    tools=[],  # Will be populated when tools are implemented
    verbose=True
)