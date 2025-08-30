from pydantic import BaseModel, Field
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


class CvTransformationPlan(BaseModel):
    job_title: str
    company: str

    # transparency on alignment
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    transferable_skills: List[str] = []

    # edit plan
    additions: List[str] = Field(
        default_factory=list, description="New bullets/sections from KB to insert"
    )
    rewrites: List[str] = Field(
        default_factory=list, description="Rewrite existing bullets for impact/fit"
    )
    removals: List[str] = Field(
        default_factory=list, description="Cut/downplay irrelevant items"
    )
    reordering: List[str] = Field(
        default_factory=list, description="Prioritize sections/experiences"
    )

    # ATS & language
    quantifications: List[str] = Field(
        default_factory=list, description="Where to add real metrics"
    )
    terminology_alignment: List[str] = Field(
        default_factory=list, description="Exact phrase swaps to match posting"
    )

    # optional traceability
    evidence: List[str] = Field(
        default_factory=list, description="KB pointers backing suggestions"
    )


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
