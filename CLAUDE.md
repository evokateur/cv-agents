# C.V. Generation and Optimization System

## C.V. Generation

Generates my CV using JSON/YAML data and a LaTeX Jinja template.

## Resume Optimizer Agent System

An agentic solution for resume optimization. It would involve processing a job
posting and extracting the information, reading from a knowledge base containing
information about the type of work I've done, evaluating how well I might fit in
the position, and finally creating an optimized C.V. data file for the generator.

### Core Task Partitions

#### 1. Job Analysis Agent

- Extract requirements, skills, qualifications from job posting
- Parse company/role context
- Output: Structured job requirements

#### 2. Knowledge Retrieval Agent  

- Query work history knowledge base
- Match relevant experiences to job requirements
- Output: Ranked relevant experiences

#### 3. Fit Assessment Agent

- Score compatibility between background and requirements
- Identify gaps and strengths
- Output: Fit analysis with recommendations

#### 4. CV Optimization Agent

- Restructure content based on job priorities
- Rewrite descriptions for relevance
- Optimize for ATS/keywords
- Output: Optimized CV (target schema)

#### 5. Orchestration Layer

- Manages agent sequencing
- Handles data flow and validation
- Error recovery

### Data Flow

```
Job Posting → Analysis → Knowledge Retrieval → Fit Assessment → CV Optimization → Schema Output
```
