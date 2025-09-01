# 📌 Project Brief: CV Optimization Pipeline (CrewAI + Pydantic)

## 🎯 Main Goal

Build a CrewAI-based system that **aligns a human-written base CV** with job postings, using a **knowledge base of projects/experiences** to generate structured, actionable edit plans. The system should evolve toward **CV transformation by vectors**:

* **JobPosting vector** (requirements, keywords, responsibilities)
* **Base CV vector** (human-written source of truth)
* **Knowledge Base vector** (projects, achievements, metrics)

The output is not a rewritten CV but a **CvTransformationPlan**: a structured diff/plan of edits to apply to the CV.

---

## 🧩 System Evolution

### Original (before changes)

1. **Job Analysis Task** → `JobPosting` (flat schema, noisy).
2. **Candidate Profiling Task** → `CandidateProfile` (marketing-oriented output with competitive advantages, positioning strategy).
3. **CV Optimization Task** → rewrote CV wholesale.

**Implicit Objective:** create marketing-style tailored CVs automatically.

---

### Revised Pipeline

1. **Job Analysis Task**

   * Improved `JobPosting` schema:

     ```python
     class JobPosting(BaseModel):
         title: str
         company: str
         industry: str
         description: str
         experience_level: str
         education: List[str] = []
         years_experience: Optional[str] = None
         hard_requirements: List[str] = []
         technical_skills: List[str] = []
         soft_skills: List[str] = []
         preferred_skills: List[str] = []
         responsibilities: List[str] = []
         keywords: List[str] = []
         tools_and_tech: List[str] = []
     ```

   * Outputs structured vectors (skills split, keywords, ATS terms).
   * Results are cleaner, action-oriented responsibilities, deduplicated keywords, graceful handling of missing fields.

2. **CV Alignment Task** *(replaces Candidate Profiling Task)*

   * Agent: `cv_adviser`
   * Task: `cv_alignment_task`
   * Model: `CvTransformationPlan`
   * Description explicitly integrates **both JobPosting + Knowledge Base**.
   * Uses SemanticSearchTool with natural-language queries.
   * **Guardrails:**

     * Do not fabricate employers/projects.
     * Cite KB evidence where possible.
     * Output is a **plan**, not a rewritten CV.

   **Schema:**

   ```python
   class CvTransformationPlan(BaseModel):
       job_title: str
       company: str
       matching_skills: List[str] = []
       missing_skills: List[str] = []
       transferable_skills: List[str] = []
       additions: List[str] = []
       rewrites: List[str] = []
       removals: List[str] = []
       reordering: List[str] = []
       quantifications: List[str] = []
       terminology_alignment: List[str] = []
       evidence: List[str] = []
   ```

   **Task Prompt Highlights:**

   * Compare JobPosting ↔ CV ↔ KB.
   * Plan edits: additions, rewrites, removals, reordering.
   * ATS: add metrics, align terminology with keywords.
   * No direct rewriting.
   * Cite KB evidence.

3. **Executor (future step)**

   * To apply `CvTransformationPlan` into:

     * A new draft CV, or
     * A structured patch (`ResumeEditPatch` style).
   * Not yet implemented — will be designed later.

---

## 🔑 Key Decisions

* Terminology: use **CV** consistently (not resume).
* Replace marketing-style `CandidateProfile` with actionable `CvTransformationPlan`.
* Separate **Planner (cv\_adviser)** from future **Executor** for clarity and traceability.
* Knowledge base documents must distinguish **Employer / Client / Project** to avoid misattribution.
* Commit counts are weak evidence → treat as **supporting evidence only**, prefer impact/outcome metrics.

---

## 🧪 Tests & Results

* Compared **old vs new JobPosting outputs** on Automattic job ad:

  * New schema produced cleaner requirements, separated technical vs soft skills, extracted keywords/tools, action-oriented responsibilities.
* Compared **old vs new candidate profiler outputs**:

  * New schema led to more concrete technical matches and domain focus, but still produced marketing-like “positioning strategy” and awkward commit/SQL line metrics.
  * Confirmed need for schema shift to transformation plan.

---

## 📌 Unresolved / Next Steps

1. **Implement cv\_adviser + cv\_alignment\_task** fully in `cv-transformer` branch.
2. **Run A/B test** of CvTransformationPlan generation on same CV + KB + JobPosting to check:

   * Are additions/rewrites grounded in KB?
   * Are responsibilities mapped directly?
   * Are quantifications realistic (impact > activity)?
3. **Refactor project doc prompts** so KB communicates employer vs project roles correctly.

   * Schema for project docs: `employer`, `client`, `project_name`, `role`, `dates`, `tech_stack`, `responsibilities`, `impact_metrics`, `evidence_sources`.
4. **Design Executor Task/Agent** that applies CvTransformationPlan into either:

   * `CurriculumVitae` model, or
   * A patch/diff representation.

---

## 🧭 Context / Constraints

* System is CrewAI-based, with Pydantic models for structured outputs.
* Tasks use YAML config for descriptions; variables (`[[JobPosting]]`, `{candidate_cv_path}`) are injected at runtime.
* Knowledge base is evolving, created via LLM prompts, needs refinement for clarity.
* CV is **human-written base document**; AI should not replace it, only suggest structured edits.
