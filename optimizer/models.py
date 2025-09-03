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
    job_title: str = Field(description="EXACT job title from the JobPosting context - use JobPosting.title exactly, do not modify or make up titles")
    company: str = Field(description="EXACT company name from the JobPosting context - use JobPosting.company exactly, never invent or modify company names")

    # transparency on alignment
    matching_skills: List[str] = Field(default_factory=list, description="Skills from candidate's CV that directly match JobPosting requirements - list specific skills found in both")
    missing_skills: List[str] = Field(default_factory=list, description="Skills explicitly required in JobPosting that are absent from candidate's CV - use exact terms from JobPosting")
    transferable_skills: List[str] = Field(default_factory=list, description="Candidate's existing skills that relate to JobPosting requirements but need repositioning or reframing")

    # edit plan
    additions: List[str] = Field(
        default_factory=list, description="Specific text snippets from knowledge base to add to CV - include exact quotes with context, e.g. 'Add bullet: Built scalable architecture supporting 5,000+ active participants (from 569trusts.md)'"
    )
    rewrites: List[str] = Field(
        default_factory=list, description="Specific CV text improvements with before/after examples, e.g. 'Change \"Backend Developer\" to \"Senior PHP Developer with WordPress expertise\" to match JobPosting requirements'"
    )
    removals: List[str] = Field(
        default_factory=list, description="Specific CV items to remove or de-emphasize - quote exact text to remove and explain why it doesn't align with JobPosting"
    )
    reordering: List[str] = Field(
        default_factory=list, description="Specific sections or experiences to reorder for better alignment - provide exact section names and new priority order"
    )

    # ATS & language
    quantifications: List[str] = Field(
        default_factory=list, description="Specific metrics from knowledge base to add to CV with exact context, e.g. 'Add \"reduced processing time by 95%\" to 569 Trusts project description'"
    )
    terminology_alignment: List[str] = Field(
        default_factory=list, description="Exact phrase replacements to match JobPosting keywords, e.g. 'Replace \"web development\" with \"PHP and JavaScript development\" to match JobPosting.technical_skills'"
    )

    # optional traceability
    evidence: List[str] = Field(
        default_factory=list, description="Specific knowledge base file paths that support the transformation recommendations, e.g. '/path/to/569trusts.md - contains PHP/Symfony experience'"
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
