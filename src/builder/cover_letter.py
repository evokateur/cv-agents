import json
import yaml
from pathlib import Path
from builder.template_env import get_tex_env


def generate_cover_letter(input_file: str, output_file: str):
    """Generate cover letter from JSON/YAML data and LaTeX template"""
    path = Path(input_file)
    with open(input_file) as f:
        if path.suffix.lower() == '.json':
            data = json.load(f)
        else:
            data = yaml.safe_load(f)

    env = get_tex_env()
    template = env.get_template("cover-letter.tex")

    rendered_tex = template.render(data)

    with open(output_file, "w") as f:
        f.write(
            rendered_tex.replace("xXposition", data["position"]).replace(
                "xXcompany", data["company"]
            )
        )
