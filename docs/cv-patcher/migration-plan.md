# CV Optimizer Migration Plan (Tiny, Human‑Verifiable Steps)

**Goal:** Evolve the current CrewAI workflow into a **schema‑first, evidence‑backed, minimal‑diff CV optimizer**.  
**Assumptions:** You will handle branching and commits yourself and will review/tweak each step before committing.  
**Code changes:** Where possible, reference the generated patch files. Adjust the paths as needed for your environment.

Patch files you can use directly (or paste from them):

- `step02_add_evidence.patch`
- `step03_skill_project_support.patch`
- `step04_extend_candidate_profile.patch`
- `step05_trp_schema.patch`
New modules to drop in:
- `optimizer/verifier.py`
- `optimizer/patcher.py`

> Optionally apply patches with: `git apply <patchpath>` or `patch -p1 < <patchpath>`  
> If a hunk fails, open the patch and paste the additions manually where indicated below.

---

## Step 1 — Baseline sanity

Make sure file paths in the patch files match the repository file structure. Fix if not.

---

## Step 2 — Add `Evidence` model (schema for citations)

**What:** Introduce a minimal citation object.  
**Do:** Apply `step02_add_evidence.patch` (or copy its class into `optimizer/models.py`).  
**Verify:**

```bash
python - <<'PY'
from optimizer.models import Evidence
e = Evidence(id="kb:doc#1", snippet="latency 220ms→60ms", confidence=0.9)
print(e.model_dump())
PY
```

**Expect:** A dict with `id`, `snippet`, optional `source_url`, `confidence`.

---

## Step 3 — Add `SkillSupport` and `ProjectSupport`

**What:** Structured containers that attach `Evidence` to skills/projects.  
**Do:** Apply `step03_skill_project_support.patch`.  
**Verify:**

```bash
python - <<'PY'
from optimizer.models import SkillSupport, ProjectSupport, Evidence
ps = ProjectSupport(name="Benefits Rewrite", bullets=["Cut p95 73%"], evidence=[Evidence(id="kb:1", snippet="...")])
print(ps.model_dump())
PY
```

**Expect:** Structured dict; no exceptions.

---

## Step 4 — Extend `CandidateProfile` (non‑breaking)

**What:** Keep existing fields; add maps + projects + risk flags.  
**Do:** Apply `step04_extend_candidate_profile.patch`.  
**Verify:**

```bash
python - <<'PY'
from optimizer.models import CandidateProfile
cp = CandidateProfile(first_name="Wesley", last_name="Hinkle", profession="Backend")
print("ok")
PY
```

**Expect:** Prints `ok`.  
**Tweak if needed:** If your existing class order differs, paste the added fields inside `CandidateProfile` manually.

---

## Step 5 — Add `TargetedResumePatch` (TRP) schema

**What:** Represents minimal diffs against the existing CV.  
**Do:** Apply `step05_trp_schema.patch`.  
**Verify:**

```bash
python - <<'PY'
from optimizer.models import TargetedResumePatch, ExperiencePatch, BulletPatch, Evidence
trp = TargetedResumePatch(experience_patches=[
  ExperiencePatch(target_role="Acme — Senior", replace_bullets=[BulletPatch(old_idx=1, new_bullet="Cut p95 73%", evidence=[Evidence(id="kb:1", snippet="...")])])
])
print("ok")
PY
```

**Expect:** Prints `ok`.

---

## Step 6 — Add `verifier.py` (TRP checks)

**What:** Basic rules: evidence presence + confidence threshold; simple keyword coverage helper.  
**Do:** Drop in `optimizer/verifier.py` (from the provided file).  
**Verify:**

```bash
python - <<'PY'
from optimizer.models import TargetedResumePatch, ExperiencePatch, BulletPatch
from optimizer.verifier import validate_trp, meets_threshold
trp = TargetedResumePatch(experience_patches=[ExperiencePatch(target_role="X", insert_bullets_after=[BulletPatch(new_bullet="hello")])])
print("errors:", validate_trp(trp))
print("coverage:", meets_threshold(trp, ["hello","world"]))
PY
```

**Expect:** One missing‑evidence error; coverage indicates `world` missing.

---

## Step 7 — Add `patcher.py` (bullet‑level skeleton)

**What:** Deterministic replace/insert for bullet lists.  
**Do:** Drop in `optimizer/patcher.py`.  
**Verify:**

```bash
python - <<'PY'
from optimizer.patcher import apply_bullets
class O: pass
def bp(old_idx=None, anchor_idx=None, new_bullet="X"):
    x = O(); x.old_idx=old_idx; x.anchor_idx=anchor_idx; x.new_bullet=new_bullet; return x
print(apply_bullets(["a","b","c"], replace=[bp(old_idx=1, new_bullet="B")], insert_after=[bp(anchor_idx=0, new_bullet="A2")]))
PY
```

**Expect:** `['a', 'A2', 'B', 'c']`

---

## Step 8 — Tighten candidate profile task (prompt)

**What:** Enforce “cite or drop” in output.  
**Do:** Edit `optimizer/config/tasks.yaml` → `candidate_profile_task.description`. Add:

```
For every skill/project/bullet, attach at least one Evidence (id/snippet/source_url).
If no evidence is found, omit the claim or add a risk flag. Output JSON ONLY.
```

**Verify:** YAML parses (no syntax errors).

---

## Step 9 — Convert strategist to TRP diff mode (prompt)

**What:** Strategist emits TRP JSON only (no full rewrites).  
**Do:** Edit `optimizer/config/tasks.yaml` → strategist task. Replace description with:

```
Produce a TargetedResumePatch (TRP) with minimal edits.
Prefer replace over insert. Preserve voice and tense from existing bullets.
Each new/changed bullet must include ≥1 Evidence. Bullets ≤ 20 words,
verb‑first, include metric or scope when possible. Return JSON ONLY.
```

**Verify:** YAML parses.

---

## Step 10 — Add a verification task (prompt)

**What:** A dedicated step to validate TRP.  
**Do:** Add `cv_verification_task` to `optimizer/config/tasks.yaml` with output format:

```
{"report": {...}, "trp": <TargetedResumePatch>}
```

Include rules: evidence required, min confidence, keyword coverage, ATS hazards.  
**Verify:** YAML parses.

---

## Step 11 — Align agents (prompt tone + constraints)

**What:** Make roles/goals match the new behavior.  
**Do:** Edit `optimizer/config/agents.yaml`:

- **candidate_profiler:** emphasize “cite or drop”, no invented metrics, JSON only.
- **cv_strategist:** minimal‑diff, voice‑preserving, TRP JSON only.
**Verify:** YAML parses.

---

## Step 12 — Wire verifier into the Crew sequence

**What:** Add the verification step after strategist.  
**Do:** Edit `optimizer/crew.py` to insert the verifier task consuming TRP and returning `{report, trp}`.  
**Verify:** Import sanity.

```bash
python - <<'PY'
import optimizer.crew as c
print("crew import ok")
PY
```

---

## Step 13 — CLI flags for dry‑run/apply (optional)

**What:** Control rendering flow.  
**Do:** Edit `optimizer/kickoff.py`: add `--dry-run` (default) and `--apply`.  

- `--dry-run`: print JSON (JPP, CP, TRP, report)
- `--apply`: write `cv_targeted.md` using the patcher
**Verify:** `python optimizer/kickoff.py --help` shows options.

---

## Step 14 — Apply TRP to Markdown (patcher integration)

**What:** End‑to‑end rendering path.  
**Do:** Extend `optimizer/patcher.py` with `apply_trp_to_markdown(original_markdown, trp)`:

- Locate target role section
- Replace/insert bullets by index
- Reorder skills; replace summary if provided
**Verify:** Small synthetic markdown string produces expected patched output.

---

## Step 15 — Unit test: verifier

**What:** Evidence presence is enforced.  
**Do:** Create `tests/test_verifier.py` with a “missing evidence” case.  
**Verify:** `pytest -q` passes.

---

## Step 16 — Unit test: patcher

**What:** Replace and insert‑after behave deterministically.  
**Do:** Create `tests/test_patcher.py` for index logic.  
**Verify:** `pytest -q` passes.

---

## Step 17 — Strategist JSON‑only guard (prompt)

**What:** Reduce parsing failures.  
**Do:** Append to strategist task description:

```
Return a single JSON object validating against the injected schema.
Do not include markdown, code fences, or explanations.
```

**Verify:** YAML parses.

---

## Step 18 — Candidate profiler: carry tool evidence fields

**What:** Ensure Evidence fields are filled from the semantic tool.  
**Do:** Note in candidate profile task: map tool’s `{id, snippet, url}` → `Evidence.{id, snippet, source_url}`.  
**Verify:** Run a small posting through the flow and confirm CP contains Evidence entries.

---

## Step 19 — Voice preservation anchors (prompt)

**What:** Match tone and cadence.  
**Do:** Append to strategist:

```
Match voice using 3 anchor bullets from the target role (verb choice, cadence, average sentence length).
```

**Verify:** Observe style alignment in output.

---

## Step 20 — Keyword coverage rule (verifier)

**What:** Alignment with the JPP.  
**Do:** In `optimizer/verifier.py`, use `meets_threshold` with `JobPosting.required_skills + preferred_skills`.  
**Verify:** A TRP missing obvious terms yields a coverage failure.

---

## Optional: Metrics and Golden Set

- Add `optimizer/metrics.py` to compute evidence density, diff size, and basic readability.
- Create a `golden/` folder with sample postings and expected outcomes.
- Add a small script to loop and print metrics.

---

## Done

At this point the system tailors an existing CV via **evidence‑backed minimal diffs**, validated by a verifier, and rendered deterministically.
