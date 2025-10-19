import yaml
import json
from pathlib import Path
from builder.template_env import get_tex_env


def generate_cv(input_file: str, output_file: str):
    """Generate CV from JSON/YAML data and LaTeX template"""
    path = Path(input_file)
    with open(input_file) as f:
        if path.suffix.lower() == '.json':
            data = json.load(f)
        else:
            data = yaml.safe_load(f)

    env = get_tex_env()
    template = env.get_template("cv.tex")

    rendered_tex = template.render(data)

    with open(output_file, "w") as f:
        f.write(rendered_tex)
