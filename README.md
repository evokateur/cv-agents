# CV Generator/Optimizer

Generates a LaTeX CV from JSON/YAML data using a Jinja2 environment that plays well with LaTeX.

Custom delimiters, you see..

|              | customized | standard jinja2 |
| ------------ | ---------- | --------------- |
| Statements   | `(# #)`    | `{% %}`         |
| Expressions  | `(( ))`    | `{{ }}`         |
| Comments     | `%( )%`    | `{# #}`         |
| Line Comment | `%%`       | `##`            |

---

It also uses CrewAI Agents & Tasks to optimize CV data for a job posting

```
Job posting URL → Job Analyst Agent → Structured job requirements
[Candidate data, Job requirements] → Candidate Profiler Agent → Structured profile for job
[Profile, Job requirements, CV] → CV Strategist → Optimized CV
```

Pydantic models define the structure of the job requirements, candidate profile, and CV output. The CV output will conform to the [schema](https://github.com/evokateur/cv-agents/blob/main/data/cv-schema.json) expected by the LaTex generator.

Abridged project directory structure:

```
.
├── config.py
├── cv-agents.ipynb
├── data
│   ├── cv-schema.json
│   ├── cv.json
│   └── cv.yaml
├── knowledge_base/ # <-- symlink
├── kickoff_crew.py
├── make-cv.py
├── optimizer
│   ├── agents.py
│   ├── config
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── crew.py
│   ├── main.py
│   ├── models.py
│   └── tasks.py
├── templates
│   ├── cover-letter.tex
│   └── cv.tex
└── texenv
    └── jinja.py
```

The Candidate Profiler queries a vector store of chunked and embedded knowledge base docs.

I keep the knowledge base in a private repository and symlink it to `knowledge_base/`

This is what it looks like (more or less)

```
knowledge-base
├── companies
│   └── frobozz-co.md
│   └── acme.md
├── developers
│   └── wesley-hinkle.md
└── projects
|   ├── magic-api-gateway.md
|   ├── zork-legacy-cms.md
|   ├── torch-saas.md
|   ├── grue-detector.md
|   ├── zorkmid-sdk.md
|   ├── anvil.md
└── skills-mapping.md
```

General setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To generate a LaTeX CV from `data/cv.yaml`, convert it to PDF, then `open` (or `xgd-open`) it:

```
make cv
```

The `cv-agents.ipynb` notebook documents the CrewAI source files, and can be used to kickoff the crew.

```
jupyter lab
```

Claude's latest [`/init`](/CLAUDE.md) probably explains all this better than I do.
