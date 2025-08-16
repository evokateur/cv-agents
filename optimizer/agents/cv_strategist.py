from config import get_config
from crewai import Agent, LLM

config = get_config()

# TODO: determine if we need any tools for CV Strategist

llm = LLM(
    model=config.cv_strategist_model,
    temperature=float(config.cv_strategist_temperature),
)

cv_strategist = Agent(
    role="Resume Strategist and CV Optimizer",
    goal="Transform candidate profile and job requirements into an optimized CV "
    "that maximizes relevance and impact for the specific role",
    tools=[],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Resume Strategist, you are expert at crafting compelling CVs that "
        "highlight the most relevant qualifications for specific roles. You understand "
        "ATS systems, keyword optimization, and how to structure content for maximum "
        "impact with both automated systems and human recruiters."
    ),
)
