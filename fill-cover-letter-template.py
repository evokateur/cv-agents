import json
from jinja2 import Environment, FileSystemLoader
import subprocess

with open("cover-letter.json") as f:
    data = json.load(f)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("cover-letter-template.tex.jinja")

rendered_tex = template.render(data)

with open("cover-letter.tex", "w") as f:
    f.write(rendered_tex)
