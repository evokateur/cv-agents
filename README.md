# CV Generator

Generates my CV from JSON/YAML data using Jinja2 templates and LaTeX.

## Template Syntax

Custom delimiters are used to avoid conflicts with LaTeX:

|              | customized | standard jinja2 |
| ------------ | ---------- | --------------- |
| Statements   | `[# #]`    | `{% %}`         |
| Expressions  | `[- -]`    | `{{ }}`         |
| Comments     | `%# #%`    | `{# #}`         |
| Line Comment | `%%`       | `##`            |

## Quick Start

```bash
# Install dependencies in virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Generate CV
make cv

## Usage

1. Edit data in `data/cv.json` or `data/cv.yaml`
2. Run `make cv` to generate PDF
3. Find output in `output/cv.pdf`

## Structure

- `data/` - CV data files (JSON/YAML)
- `templates/` - LaTeX templates
- `output/` - Generated PDFs
- `examples/` - Template examples
