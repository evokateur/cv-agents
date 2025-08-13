from pydantic import BaseModel
from typing import List, Dict, Any


class JobPosting(BaseModel):
    title: str
    company: str
    industry: str
    description: str
    experience_level: str
    requirements: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
