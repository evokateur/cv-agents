import json

def json_to_latex_template(json_data, template_file="cover-letter-template.tex", output_file="cover-letter.tex"):
    with open(template_file, "r") as file:
        template = file.read()
    
    template = template.replace("xXname", json_data["name"])
    template = template.replace("xXemail", json_data["contact"]["email"])
    template = template.replace("xXphone", json_data["contact"]["phone"])
    template = template.replace("xXphone", json_data["contact"]["phone"])
    template = template.replace("xXintroduction", json_data["introduction"])
    template = template.replace("xXeducation", json_data["education"])
    template = template.replace("xXqualities", json_data["qualities"])
    template = template.replace("xXexperience", json_data["experience"])
    template = template.replace("xXclosing", json_data["closing"])
    
    with open(output_file, "w") as file:
        file.write(template)

with open("cover-letter.json", "r") as file:
    cover_letter_data = json.load(file)
    json_to_latex_template(cover_letter_data)
