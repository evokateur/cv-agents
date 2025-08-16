from config import get_config
from crewai import Agent, LLM
from crewai_tools import RagTool

config = get_config()

# TODO: figure out how we want to instantiate and configure the RagTool
rag_tool = RagTool(
    config=dict(
        llm=dict(
            provider="aws_bedrock",
            config=dict(
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            ),
        ),
        embedder=dict(
            provider="aws_bedrock",
            config=dict(
                model="amazon.titan-embed-text-v1",
                task_type="retrieval_query",
            ),
        ),
    )
)

llm = LLM(
    model=config.candidate_profiler_model,
    temperature=float(config.candidate_profiler_temperature),
)

candidate_profiler = Agent(
    role="Candidate Profiler",
    goal="Extract and synthesize relevant professional experience from knowledge base "
    "to create a compelling candidate profile tailored to job requirements",
    tools=[rag_tool],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Knowledge Base Profiler, you excel at semantic search through "
        "professional histories to uncover relevant experiences that align "
        "with specific job opportunities, even when connections aren't obvious."
    ),
)
