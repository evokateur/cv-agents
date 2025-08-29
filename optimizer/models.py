from pydantic import BaseModel
from typing import List, Optional


class JobPosting(BaseModel):
    # Basic metadata
    title: str
    company: str
    industry: str
    description: str
    experience_level: str  # entry, mid, senior, etc.

    # Requirements
    education: List[str] = []  # degrees, certifications
    years_experience: Optional[str] = None  # "5+ years"
    hard_requirements: List[str] = []  # absolute musts (e.g., "CPA license")

    # Skills (structured)
    technical_skills: List[str] = []  # e.g., "Python", "AWS", "GraphQL"
    soft_skills: List[str] = []  # e.g., "leadership", "teamwork"
    preferred_skills: List[str] = []  # nice-to-have

    # Responsibilities
    responsibilities: List[str] = []  # parsed job duties

    # Extracted for ATS alignment
    keywords: List[str] = []  # important phrases/terms from posting
    tools_and_tech: List[str] = []  # specific stack/tools


class CandidateProfile(BaseModel):
    first_name: str
    last_name: str
    profession: str

    matching_required_skills: List[str]
    matching_preferred_skills: List[str]
    transferable_skills: List[str]
    skill_gaps: List[str]

    relevant_experiences: List[str]
    relevant_projects: List[str]
    leadership_examples: List[str]
    domain_expertise: List[str]

    quantified_achievements: List[str]
    technical_achievements: List[str]
    career_progression: List[str]

    competitive_advantages: List[str]
    value_propositions: List[str]
    positioning_strategy: str


class Contact(BaseModel):
    city: str
    state: str
    email: str
    phone: str
    linkedin: str
    github: str


class Education(BaseModel):
    degree: str
    coursework: str
    institution: str
    location: str
    start_date: str
    end_date: str


class Experience(BaseModel):
    title: str
    company: str
    location: str
    start_date: str
    end_date: str
    responsibilities: Optional[List[str]] = None


class AdditionalExperience(BaseModel):
    title: str
    company: str
    location: str
    start_date: str
    end_date: str


class AreaOfExpertise(BaseModel):
    name: str
    skills: List[str]


class Language(BaseModel):
    language: str
    level: str


class CurriculumVitae(BaseModel):
    name: str
    contact: Contact
    profession: str
    core_expertise: List[str]
    summary_of_qualifications: List[str]
    education: List[Education]
    experience: List[Experience]
    additional_experience: List[AdditionalExperience]
    areas_of_expertise: List[AreaOfExpertise]
    languages: List[Language]
