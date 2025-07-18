import json
from texenv.jinja import get_tex_env

with open("cv.json") as f:
    data = json.load(f)

env = get_tex_env()
template = env.get_template("cv-template.tex")

rendered_tex = template.render(data)

with open("cv.tex", "w") as f:
    f.write(rendered_tex)
