import yaml
import json
import argparse
from pathlib import Path
from texenv.jinja import get_tex_env

def main():
    parser = argparse.ArgumentParser(description="Generate CV from JSON/YAML data and LaTeX template")
    parser.add_argument("input_file", help="Path to input JSON or YAML file")
    parser.add_argument("output_file", help="Path to output LaTeX file")
    
    args = parser.parse_args()
    
    # Load data based on file extension
    path = Path(args.input_file)
    with open(args.input_file) as f:
        if path.suffix.lower() == '.json':
            data = json.load(f)
        else:  # assume YAML for .yaml, .yml, or any other extension
            data = yaml.safe_load(f)
    
    env = get_tex_env()
    template = env.get_template("cv.tex")
    
    rendered_tex = template.render(data)
    
    with open(args.output_file, "w") as f:
        f.write(rendered_tex)

if __name__ == "__main__":
    main()
