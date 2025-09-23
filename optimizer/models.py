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

    # PRIMARY TARGET FIELD MODIFICATIONS (schema-aware, highest impact)
    profession_optimization: Optional[str] = Field(
        default=None, description="New profession field value to better align with job title, e.g. 'Senior PHP Developer' instead of 'Full Stack Developer'"
    )

    core_expertise_changes: List[str] = Field(
        default_factory=list, description="Specific core_expertise field modifications with knowledge base evidence, e.g. 'Move \"PHP Development\" to first position based on job requirements' or 'Add \"WordPress Development\" based on 569trusts.md experience'"
    )

    summary_qualification_rewrites: List[str] = Field(
        default_factory=list, description="Specific summary_of_qualifications bullet point rewrites with before/after examples and knowledge base citations, e.g. 'Replace \"Experienced developer\" with \"Senior PHP developer with 8+ years building scalable web applications (see 569trusts.md, projectx.md)\"'"
    )

    experience_responsibility_updates: List[str] = Field(
        default_factory=list, description="Specific experience[].responsibilities bullet updates with job index, responsibility index, and knowledge base evidence, e.g. 'Experience[0].responsibilities[1]: Change to \"Developed REST APIs using PHP/Symfony serving 5,000+ users\" (from 569trusts.md)'"
    )

    # ATS & quantification enhancements
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
