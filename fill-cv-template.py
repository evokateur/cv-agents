import json
from jinja2 import Environment, FileSystemLoader

with open("cv.json") as f:
    data = json.load(f)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("cv-template.tex.jinja")

rendered_tex = template.render(data)

with open("cv.tex", "w") as f:
    f.write(rendered_tex)
