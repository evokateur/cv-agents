from typing import List

def apply_bullets(bullets: List[str], replace=[], insert_after=[]):
    """Apply bullet-level patches deterministically.
    - replace: objects with .old_idx and .new_bullet
    - insert_after: objects with .anchor_idx and .new_bullet
    Returns a new list.
    """
    b = bullets[:]
    # Replace by index
    for bp in replace:
        if getattr(bp, 'old_idx', None) is not None and 0 <= bp.old_idx < len(b):
            b[bp.old_idx] = bp.new_bullet
    # Insert after anchor (track offset as we insert)
    offset = 0
    for bp in insert_after:
        if getattr(bp, 'anchor_idx', None) is not None and 0 <= bp.anchor_idx < len(b):
            idx = bp.anchor_idx + 1 + offset
            b.insert(idx, bp.new_bullet)
            offset += 1
    return b
