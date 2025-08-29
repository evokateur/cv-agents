from pydantic import BaseModel
from typing import Dict, List, Literal, Optional


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


    # --- structured maps (added) ---
    matching_required_skills_map: Dict[str, SkillSupport] = {}
    matching_preferred_skills_map: Dict[str, SkillSupport] = {}
    transferable_skills_map: Dict[str, SkillSupport] = {}
    projects: List[ProjectSupport] = []
    risk_flags: List[str] = []

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


class Evidence(BaseModel):
    id: str
    snippet: str
    source_url: Optional[str] = None
    confidence: float = 0.8


class SkillSupport(BaseModel):
    level: Literal["expert","advanced","intermediate","familiar"]
    evidence: List[Evidence] = []


class ProjectSupport(BaseModel):
    name: str
    role: Optional[str] = None
    stack: List[str] = []
    bullets: List[str] = []
    evidence: List[Evidence] = []


class BulletPatch(BaseModel):
    old_idx: Optional[int] = None
    anchor_idx: Optional[int] = None
    new_bullet: str
    evidence: List[Evidence] = []


class ExperiencePatch(BaseModel):
    target_role: str
    replace_bullets: List[BulletPatch] = []
    insert_bullets_after: List[BulletPatch] = []


class TargetedResumePatch(BaseModel):
    summary_rewrite: Optional[str] = None
    experience_patches: List[ExperiencePatch] = []
    skills_reorder: Optional[List[str]] = None
    remove_sections: List[str] = []
    ats_checks: Dict[str, bool] = {}
