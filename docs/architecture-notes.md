# Architecture Notes

## Candidate Profiler Tool Architecture Summary

### RagTool

Give the agent a `RagTool` that

- uses existing ChromaDB vector store if available
- builds the vector store from kb docs if missing or invalid
- separates concerns of embedding and querying
- uses configurable LLM for semantic retrieval

#### Components

##### `utils/vector_utils.py`

- validates ChromDB vector store
- can clobber a vector store
- can print vector DB info

##### `VectorDbBuilder`

- handles vector DB creation
- skips creation if valid DB exists
- supports forced rebuilds

##### `get_rag_tool` function in `agents.py`

- uses the components above to manage and validate the vector store

### DirectoryReadTool

Give the agent access to the knowledge base directory to

- retrieve full documents when a semantic chunk is interesting but incomplete
- understand project or skill context beyond summarized chroma-embeddings
- bridge RAG output with original source materials

## Putting Pydantic Schema in Prompts

>"*It was sending the bones!*"

The vector database was being created correctly, but the candidate profiler
was not using it correctly. It was taking the structured output it received and
sending chunks of it as queries. The RAG tool expects natural language
language queries for semantic search. Prompting it to use natural language
wasn't going to fix the problem, since it didn't know where to look for meaning[^1].
All it could do was send random parts (unnatural queries) and hope for the best.

[^1]: The CrewAI Assistant says a very sophisticated model could pull it off
(but we get what we pay for, around here).

To fix this we have to create the task description dynamically, injecting
the relevant schema information for any task that receives structured output
from the previous task[^2].

[^2]: An `input_pydantic` parameter exists but setting it does not expose the
schema to the agent. It's only used for validation (and cannot specify more
than one type).  

The description starts as a template with placeholders for the schema, then
it's sent to a helper function that injects the Pydantic schema information
in right places, i.e. `[[JobPosting]]`. I chose those delimiters so future
me will not confuse them with the normal sort of variable placeholders found
in task descriptions.

YAML is still used for the tasks, with a temporary description indicating
what's to come.

### New thing

#### `utils/prompt_utils.py`

- a function to inject a Pydantic schema into text
- a function to fill all placeholders in a block of text

### Addendum

You can keep the description as a template in the YAML, get it from the
object created from the YAML, inject the schema, then override the description
with the result as before.

Looks a lot nicer.

## Giving the Profiler Access to KB Docs

After finally asking the right questions, I found out that the CrewAI RAG tool
will not give the agent the source of the chunks it returns. And so, a tool
was created that does. The agent now has the full path of the source document
and can just use the FileReadTool, if it can be coaxed to do so, somehow.

## New Objective

It looks like the system has become something other than what I intended.

According to GPT-5, the current system's implicit objective:

> Fully automate CV rewriting into an ATS-friendly version, leaning heavily on marketing-speak.

And my actual objective (restated coherently) is:

> Guide transformations of an authentic, human-written base resume by:
>
> - Mapping job requirements to what’s in your knowledge base.
> - Suggesting changes/additions/deletions to the base doc, not rewriting it wholesale.
> - Keeping the human voice/style intact, while progressively enriching the base resume over time.

Stated incoherently:

>I am starting with a human written resume and cover letter.
>
> Things that I would want:
>
> 1. Based on \[...\] stuff that I will put into a knowledge base (a work in
> progress, more knowledge, more ways to get \[to\] it to come) how should a change
> \[be made\] the base resume to align it with the requirements of a particular job
> 2. \[Later\] how should the base resume evolve when more information becomes
> available in usable ways from my knowledge base
>
> The job posting is like a vector that shapes the direction of the resume.
> It's just one job posting for now. It's a start. I could also use more than
> one, an arbitrary set, of job requirements to push the direction of the resume
> into a more coalesced direction...
>
> So anyway, the two things I'm working on right now are 1 job posting + a
> growing knowledge base. I will get back to pushing the original resume in
> some direction once I've nailed this down.

The new, proposed workflow:

### Job Analysis

Same general thing, but better output schema and prompts. We've already done this and seen the effect it has on the work of the (soon to be disappeared) Candidate Profier.

Then we really start chasing the dragon

> ### Planner (produces `ResumeTransformationPlan`)
>
> - **Goal:** Decide *what should change* in the base resume to align with the job.
> - **Inputs:** `JobPosting` (structured), base resume, KB.
> - **Output (JSON plan):** Concrete, human-readable directives:
>
>   - `additions` — what new items to add from KB (projects, tools, metrics)
>   - `rewrites` — how to rephrase existing bullets (impact/scale/keywords)
>   - `removals` — what to drop or de-emphasize
>   - `reordering` — what to move up/down
>   - `terminology_alignment` — exact phrasing swaps to match posting
>   - `quantifications` — where to inject real metrics
>   - (optional) `evidence` — KB pointers used for each suggestion
> - **Contract:** No rewriting the resume here. No invented facts. It’s a **diff-like plan**.
>
> ### Executor (applies the plan → produces artifacts)
>
> You can design this as one task or a few small ones, but its job is to **apply** the plan.
>
> - **Goal:** Turn the plan into concrete outputs you can ship or review.
>
> - **Inputs:** `ResumeTransformationPlan`, base resume (source of truth), KB.
>
> - **Outputs (choose one or several):**
>
>   1. **Patched Resume** (same format as the base, e.g., JSON/YAML/Markdown)
>
>      - Applies `additions/rewrites/removals/reordering` to produce a *drafted* tailored resume.
>   2. **Patch File** (safer, human-in-the-loop):
>
>      - JSON Patch / unified diff / PR-style change set you can review.
>   3. **Section Drafts**:
>
>      - Only drafts the specific bullets/sections listed in the plan (no whole-doc rewrite).
>   4. **Collateral** (optional follow-ons):
>
>      - Cover-letter bullet points, LinkedIn tweaks, interview talking points — all *sourced from the same plan*.
>
> - **Contract/Guardrails:**
>
>   - Must only use facts present in base resume or KB (no fabrication).
>   - If a plan item lacks evidence, executor should **skip** or mark it for review.
>   - Preserve original voice/format unless the plan says otherwise.
>
> ### Why split them?
>
> - **Traceability:** You can inspect/approve the plan before any edits happen.
> - **Reusability:** One plan can drive multiple artifacts (resume, cover letter, LinkedIn).
> - **Safety:** Executor is constrained by the plan + evidence; fewer hallucinations.
> - **Iteration:** If you dislike a suggestion, fix the plan and re-apply — deterministic changes.
