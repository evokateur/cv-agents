from typing import List, Tuple
from optimizer.models import TargetedResumePatch

MIN_CONFIDENCE = 0.6

def validate_trp(trp: TargetedResumePatch) -> List[str]:
    errors: List[str] = []
    # Evidence required on every changed/inserted bullet
    for ep in trp.experience_patches:
        role = ep.target_role
        for bp in (ep.replace_bullets + ep.insert_bullets_after):
            if not bp.evidence:
                errors.append(f"Missing evidence for bullet in role '{role}' -> '{bp.new_bullet[:60]}'")
            else:
                if all((ev.confidence or 0.0) < MIN_CONFIDENCE for ev in bp.evidence):
                    errors.append(f"Low-confidence evidence (<{MIN_CONFIDENCE}) for bullet in role '{role}'")
    return errors

def meets_threshold(trp: TargetedResumePatch, required_terms: List[str]) -> Tuple[bool, List[str]]:
    text_parts: List[str] = []
    for ep in trp.experience_patches:
        for bp in (ep.replace_bullets + ep.insert_bullets_after):
            text_parts.append(bp.new_bullet.lower())
    blob = " ".join(text_parts)
    missing = [t for t in required_terms if t.lower() not in blob]
    return (len(missing) == 0, missing)
