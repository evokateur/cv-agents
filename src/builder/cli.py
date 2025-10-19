import argparse
from builder.generator import generate_cv
from builder.cover_letter import generate_cover_letter


def main_cv():
    """CLI entry point for CV generation"""
    parser = argparse.ArgumentParser(description="Generate CV from JSON/YAML data and LaTeX template")
    parser.add_argument("input_file", help="Path to input JSON or YAML file")
    parser.add_argument("output_file", help="Path to output LaTeX file")

    args = parser.parse_args()
    generate_cv(args.input_file, args.output_file)


def main_cover_letter():
    """CLI entry point for cover letter generation"""
    parser = argparse.ArgumentParser(description="Generate cover letter from JSON/YAML data and LaTeX template")
    parser.add_argument("input_file", help="Path to input JSON or YAML file")
    parser.add_argument("output_file", help="Path to output LaTeX file")

    args = parser.parse_args()
    generate_cover_letter(args.input_file, args.output_file)


if __name__ == "__main__":
    main_cv()
