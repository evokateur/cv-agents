import re
from jinja2 import Environment, FileSystemLoader


def escape_tex(text):
    if not isinstance(text, str):
        return text
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
    return pattern.sub(lambda match: replacements[match.group()], text)


def get_tex_env(template_dir="templates"):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string=r"(#",
        block_end_string="#)",
        variable_start_string=r"((",
        variable_end_string="))",
        line_comment_prefix=r"%%",
        comment_start_string=r"%(",
        comment_end_string=")%",
    )
    env.filters["escape_tex"] = escape_tex
    return env
