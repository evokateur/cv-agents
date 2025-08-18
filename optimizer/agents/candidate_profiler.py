from config import get_config
from crewai import Agent, LLM
from crewai_tools import FileReadTool
from optimizer.tools import knowledge_base_rag_tool

config = get_config()

file_read_tool = FileReadTool()

llm = LLM(
    model=config.candidate_profiler_model,
    temperature=float(config.candidate_profiler_temperature),
)

candidate_profiler = Agent(
    role="Candidate Profiler",
    goal="Extract and synthesize relevant professional experience from knowledge base "
    "to create a compelling candidate profile tailored to job requirements",
    tools=[knowledge_base_rag_tool, file_read_tool],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Knowledge Base Profiler, you excel at semantic search through "
        "professional histories to uncover relevant experiences that align "
        "with specific job opportunities. When RAG chunks reveal interesting details, "
        "you dive deeper by reading full documents to understand complete context "
        "and extract comprehensive insights about projects, achievements, and skills."
    ),
)
