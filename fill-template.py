import json

def json_to_latex_template(json_data, template_file="template.tex", output_file="cv.tex"):
    with open(template_file, "r") as file:
        template = file.read()
    
    template = template.replace("xXname", json_data["name"])
    template = template.replace("xXemail", json_data["contact"]["email"])
    template = template.replace("xXphone", json_data["contact"]["phone"])
    template = template.replace("xXsummary", json_data["summary"])
    
    education_items = "\n".join(
        [f"\\item {edu['degree']} at {edu['institution']} ({edu['start_date']} -- {edu['end_date']})" 
         for edu in json_data["education"]]
    )
    template = template.replace("xXeducation", education_items)
    
    experience_items = "\n".join(
        [
            f"\\item \\textbf{{{exp['title']}}} at {exp['company']} ({exp['start_date']} -- {exp['end_date']})\n"
            + "  \\begin{itemize}[leftmargin=*]\n"
            + "\n".join([f"    \\item {resp}" for resp in exp["responsibilities"]])
            + "\n  \\end{itemize}"
            for exp in json_data["experience"]
        ]
    )
    template = template.replace("xXexperience", experience_items)
    
    skills = ", ".join(json_data["skills"])
    template = template.replace("xXskills", skills)

    languages_items = "\n".join(
        [f"\\item {lang['language']} ({lang['level']})" 
         for lang in json_data["languages"]]
    )
    template = template.replace("xXlanguages", languages_items)
    
    with open(output_file, "w") as file:
        file.write(template)

with open("cv.json", "r") as file:
    cv_data = json.load(file)
    json_to_latex_template(cv_data)
