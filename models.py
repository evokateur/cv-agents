from pydantic import BaseModel
from typing import List, Dict, Any


class JobPosting(BaseModel):
    title: str
    company: str
    requirements: List[str]
    skills: List[str]
    experience_level: str
    industry: str
    description: str


class KnowledgeItem(BaseModel):
    content: str
    relevance_score: float
    source_file: str
    metadata: Dict[str, Any]


class FitAssessment(BaseModel):
    overall_score: float
    skill_matches: List[Dict[str, Any]]
    experience_relevance: float
    gaps: List[str]
    strengths: List[str]


class CVData(BaseModel):
    # Conforms to existing CV schema
    personal_info: Dict[str, str]
    experience: List[Dict[str, Any]]
    skills: List[str]
    education: List[Dict[str, Any]]