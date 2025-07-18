import json
from jinja2 import Environment, FileSystemLoader


def get_tex_env():
    return Environment(
        loader=FileSystemLoader("."),
        block_start_string="(%",
        block_end_string="%)",
        variable_start_string="((",
        variable_end_string="))",
        comment_start_string="(#",
        comment_end_string="#)",
    )


with open("cv.json") as f:
    data = json.load(f)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("cv-template.tex.jinja")

rendered_tex = template.render(data)

with open("cv.tex", "w") as f:
    f.write(rendered_tex)
