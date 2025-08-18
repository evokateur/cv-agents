# CV Generator/Optimizer

Generates a LaTeX CV from JSON/YAML data using a Jinja template with custom delimiters that play well with LaTeX syntax.

|              | customized | standard jinja2 |
| ------------ | ---------- | --------------- |
| Statements   | `(# #)`    | `{% %}`         |
| Expressions  | `(( ))`    | `{{ }}`         |
| Comments     | `%( )%`    | `{# #}`         |
| Line Comment | `%%`       | `##`            |

---

Uses CrewAI Agents & Tasks to optimize the base CV data for a job posting

```
Job posting URL → Job Analyst Agent → Structured job requirements
[Candidate data, Job requirements] → Candidate Profiler Agent → Structured profile for job
[Profile, Job requirements] → CV Strategist → Optimized CV (data)
```

Pydantic models are used to define the structure of the job posting, candidate profile, and CV (<-- based on `cv-schema.json`).

The Candidate Profiler uses the CrewAI RagTool to query a vector DB containing chunked and embedded knowledge base data.

(I currently keep the knowledge base in a private repository and symlink it to `knowledge_base/`)

Project directory structure (abridged)

```
.
├── config.py
├── data
│   ├── cv-schema.json
│   ├── cv.json
│   ├── cv.yaml
├── knowledge_base/ # <-- symlink
├── make-cv.py
├── optimizer
│   ├── agents
│   │   ├── candidate_profiler.py
│   │   ├── cv_strategist.py
│   │   └── job_analyst.py
│   ├── crew.py
│   ├── models.py
│   ├── tasks
│   │   ├── candidate_profiling_task.py
│   │   ├── cv_optimization_task.py
│   │   └── job_analysis_task.py
│   └── tools
│       └── knowledge_base_rag_tool.py
├── templates
│   ├── cover-letter.tex
│   └── cv.tex
└── texenv
    └── jinja.py
```

General setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To generate a LaTeX CV, convert it to PDF, and open it

```
make cv
```

The `cv-agents.ipynb` notebook coordinates the optimization pipeline for now

```
jupyter lab
```

[Claude](/CLAUDE.md) probably explains all this better than I do.
