import json
from jinja2 import Environment, FileSystemLoader
import subprocess

# Load JSON data
with open("cv.json") as f:
    data = json.load(f)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))  
template = env.get_template("cv-template.tex.jinja")

# Render the template
rendered_tex = template.render(data)

# Save the rendered LaTeX file
with open("cv.tex", "w") as f:
    f.write(rendered_tex)

# Compile LaTeX to PDF using pdflatex
# subprocess.run(["pdflatex", "resume_output.tex"])
