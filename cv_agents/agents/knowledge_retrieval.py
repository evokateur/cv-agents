from crewai import Agent


knowledge_retrieval_agent = Agent(
    role="Experience Retrieval Specialist",
    goal="Find relevant work experiences from knowledge base that match job requirements",
    backstory="Specialist in semantic search and matching job requirements to past experiences",
    tools=[],  # Will be populated when tools are implemented
    verbose=True
)