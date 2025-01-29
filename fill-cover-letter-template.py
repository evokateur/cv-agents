import json

def json_to_latex_template(json_data, template_file="cover-letter-template.tex", output_file="cover-letter.tex"):
    with open(template_file, "r") as file:
        template = file.read()
    
    template = template.replace("xXname", json_data["name"])
    template = template.replace("xXcity", json_data["contact"]["city"])
    template = template.replace("xXstate", json_data["contact"]["state"])
    template = template.replace("xXemail", json_data["contact"]["email"])
    template = template.replace("xXphone", json_data["contact"]["phone"])
    template = template.replace("xXphone", json_data["contact"]["phone"])

    paragraphs = ""
    for paragraph in json_data["paragraphs"]:
        paragraphs += paragraph + "\n\n"
        
    template = template.replace("xXparagraphs", paragraphs)
    
    with open(output_file, "w") as file:
        file.write(template)

with open("cover-letter.json", "r") as file:
    cover_letter_data = json.load(file)
    json_to_latex_template(cover_letter_data)
