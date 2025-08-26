import re
from typing import Dict, Type
from pydantic import BaseModel


def describe_pydantic_model_for_prompt(model_class: Type[BaseModel]) -> str:
    """
    Generate a natural-language-friendly description of a Pydantic model for use in LLM prompts.

    Args:
        model_class: A subclass of BaseModel (e.g. JobPosting, CandidateProfile)

    Returns:
        A formatted string listing field names, types, and any available descriptions.
    """
    lines = []
    for name, field_info in model_class.model_fields.items():
        type_str = _format_type(field_info.annotation)
        description = field_info.description or ""
        line = f"- {name} ({type_str})"
        if description:
            line += f": {description}"
        lines.append(line)
    return "\n".join(lines)


def _format_type(type_obj) -> str:
    """
    Return a readable type string (e.g. List[str], Dict[str, Any])
    """
    try:
        return str(type_obj).replace("typing.", "")
    except Exception:
        return str(type_obj)


def render_pydantic_models_in_prompt(
    template: str, model_registry: Dict[str, Type[BaseModel]]
) -> str:
    """
    Replaces [[ModelName]] placeholders with schema descriptions. Leaves {var} untouched.
    """

    def replacement(match):
        key = match.group(1)
        if key in model_registry:
            return describe_pydantic_model_for_prompt(model_registry[key])
        else:
            return match.group(0)  # leave unrecognized tokens unchanged

    return re.sub(r"\[\[([A-Za-z_][A-Za-z0-9_]*)\]\]", replacement, template)
