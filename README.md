# CV Generator

Generates my CV using JSON/YAML data and a LaTeX Jinja template.

## Template Syntax

Custom delimiters are used to avoid conflicts with LaTeX:

|              | customized | standard jinja2 |
| ------------ | ---------- | --------------- |
| Statements   | `(# #)`    | `{% %}`         |
| Expressions  | `(( ))`    | `{{ }}`         |
| Comments     | `%( )%`    | `{# #}`         |
| Line Comment | `%%`       | `##`            |

## Quick Start

```bash
# Install dependencies in virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Generate CV
make cv

## Structure

- `data/` - CV data files (JSON/YAML)
- `templates/` - LaTeX templates
- `output/` - Generated PDFs
- `examples/` - Template examples
