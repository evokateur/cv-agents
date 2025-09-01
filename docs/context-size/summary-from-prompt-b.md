# 📌 Conversation Summary

## Core Problem / Topic

* Building a **CrewAI-based tool** to tailor a **human-written CV** to specific job postings, guided by a growing **knowledge base (KB)**.
* The current system overemphasizes “marketing-style” candidate profiles; the real goal is **actionable transformation plans** for the CV.

---

## Objectives & Goals

1. **Short-term:**

   * Improve the **JobPosting schema** to better structure job ads for downstream tasks.
   * Replace the current **CandidateProfile** stage with a task that produces a **CvTransformationPlan** (edit instructions, not a rewritten CV).

2. **Long-term:**

   * Enable **resume evolution**: base CV updated progressively as KB grows.
   * Treat job postings as “vectors” shaping the CV, with the KB as supporting data.
   * Build separation of concerns:

     * **Planner** → produces a structured edit plan.
     * **Executor** → applies the plan to generate tailored CV drafts/patches.

---

## Crucial Decisions

* Use **“CV”** terminology consistently (not “resume”).
* Adopt naming:

  * Agent: `cv_adviser`
  * Task: `cv_alignment_task`
  * Model: `CvTransformationPlan`
* Improved **JobPosting schema**: now includes `technical_skills`, `soft_skills`, `hard_requirements`, `keywords`, `tools_and_tech`, etc.
* Confirmed: **structured job posting input** produces more concrete profiler outputs.
* Agreed: **CandidateProfile schema is misaligned** (too marketing-focused). Will be replaced with **CvTransformationPlan**.

---

## Important Facts & Constraints

* Base CV and cover letter are **human-written** starting points.
* KB is curated, evolving, and must disambiguate **employer vs project vs client**.
* Guardrails:

  * Do not fabricate employers, roles, or dates.
  * Use only facts from base CV or KB.
  * Commit counts/lines of code are weak metrics; prefer impact metrics.
* System design:

  * **JobPosting** → parsed vector of requirements.
  * **CvTransformationPlan** → structured diff-like plan.
  * Future **Executor** will apply the plan to the CV.

---

## Action Items

* ✅ (Done) Improved JobPosting schema and task (`job_analysis_task`) tested.
* ✅ (Done) Created new branch `cv-transformer` to implement next stage.
* 🔄 (In Progress) Replace CandidateProfile with CvTransformationPlan model, `cv_adviser` agent, and `cv_alignment_task`.
* 🔜 Redo KB project document prompts to clearly separate employers, clients, and projects, and surface impact metrics.
* 🔜 (Later) Build Executor task to apply CvTransformationPlan to base CV.
* 🔜 (Optional) Visualize the “vector” metaphor: job posting + KB + base CV combined into transformation vector.

---

## Context & Background

* Current profiler misclassified some **projects as employers** → KB doc generation prompts need refinement.
* User created test branches to compare old vs new job posting outputs, confirming improvements.
* Terminology: “vector math” analogy adopted — multiple input vectors (JobPosting, base CV, KB) collapse into a transformation vector for CV alignment.

---

## Established Persona / Instructions

* Assistant acts as:

  * **Expert system designer** for LLM pipelines.
  * **Practical recruiter/coach voice** for CV content.
  * **Summarizer/clarifier** when requested.
* Style: precise, structured, avoids filler, emphasizes **actionable guidance**.
