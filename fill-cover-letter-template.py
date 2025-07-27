import json
from texenv.jinja import get_tex_env

with open("data/cover-letter.json") as f:
    data = json.load(f)

env = get_tex_env()
template = env.get_template("cover-letter-template.tex")

rendered_tex = template.render(data)

with open("output/cover-letter.tex", "w") as f:
    f.write(
        rendered_tex.replace("xXposition", data["position"]).replace(
            "xXcompany", data["company"]
        )
    )
