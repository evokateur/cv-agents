import json

def json_to_latex_template(json_data, template_file="template.tex", output_file="resume.tex"):
    # Load the LaTeX template
    with open(template_file, "r") as file:
        template = file.read()
    
    # Replace placeholders with JSON data
    template = template.replace("{{name}}", json_data["name"])
    template = template.replace("{{email}}", json_data["contact"]["email"])
    template = template.replace("{{phone}}", json_data["contact"]["phone"])
    template = template.replace("{{linkedin}}", json_data["contact"]["linkedin"])
    template = template.replace("{{github}}", json_data["contact"]["github"])
    template = template.replace("{{summary}}", json_data["summary"])
    
    # Generate education section
    education_items = "\n".join(
        [f"\\item {edu['degree']} from {edu['institution']} ({edu['start_date']} -- {edu['end_date']})" 
         for edu in json_data["education"]]
    )
    template = template.replace("{{education}}", education_items)
    
    # Generate experience section
    experience_items = "\n".join(
        [
            f"\\item \\textbf{{{exp['title']}}} at {exp['company']} ({exp['start_date']} -- {exp['end_date']})\n"
            + "  \\begin{itemize}[leftmargin=*]\n"
            + "\n".join([f"    \\item {resp}" for resp in exp["responsibilities"]])
            + "\n  \\end{itemize}"
            for exp in json_data["experience"]
        ]
    )
    template = template.replace("{{experience}}", experience_items)
    
    # Generate skills section
    skills = ", ".join(json_data["skills"])
    template = template.replace("{{skills}}", skills)
    
    # Generate projects section
    project_items = "\n".join(
        [f"\\item \\textbf{{{proj['name']}}}: {proj['description']} \\href{{{proj['link']}}}{{Link}}" 
         for proj in json_data["projects"]]
    )
    template = template.replace("{{projects}}", project_items)
    
    # Write to output LaTeX file
    with open(output_file, "w") as file:
        file.write(template)

# Example usage
with open("resume.json", "r") as file:
    resume_data = json.load(file)
    json_to_latex_template(resume_data)
