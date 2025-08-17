from config import get_config
from crewai import Agent, LLM
from crewai_tools import FileReadTool

data_reader = FileReadTool()

config = get_config()

llm = LLM(
    model=config.cv_strategist_model,
    temperature=float(config.cv_strategist_temperature),
)

cv_strategist = Agent(
    role="Resume Strategist and CV Optimizer",
    goal="Transform existing CV content using job requirements and candidate profile "
    "to create an optimized version tailored to the specific role",
    tools=[data_reader],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Resume Strategist, you are expert at crafting compelling CVs that "
        "highlight the most relevant qualifications for specific roles. You understand "
        "ATS systems, keyword optimization, and how to structure content for maximum "
        "impact with both automated systems and human recruiters."
    ),
)
