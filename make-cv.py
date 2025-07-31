import yaml
from texenv.jinja import get_tex_env

with open("data/cv.yaml") as f:
    data = yaml.safe_load(f)

env = get_tex_env()
template = env.get_template("cv.tex")

rendered_tex = template.render(data)

with open("output/cv.tex", "w") as f:
    f.write(rendered_tex)
