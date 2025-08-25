import os
import shutil

CHROMA_REQUIRED_FILES = [
    "chroma-collections.parquet",
    "chroma-embeddings.parquet",
    "index",
    "chroma-lock",
]


def is_valid_chroma_vector_db(path: str) -> bool:
    """Check if a directory looks like a valid Chroma vector DB."""
    return all(os.path.exists(os.path.join(path, f)) for f in CHROMA_REQUIRED_FILES)


def delete_vector_db(path: str) -> None:
    """Delete the vector DB directory (use with caution)."""
    if os.path.exists(path):
        print(f"🧨 Deleting vector DB at {path}")
        shutil.rmtree(path)
    else:
        print(f"⚠️ Vector DB path does not exist: {path}")


def print_vector_db_info(path: str) -> None:
    """Prints basic info about the vector DB state."""
    print(f"🔍 Checking vector DB at: {path}")
    for f in CHROMA_REQUIRED_FILES:
        f_path = os.path.join(path, f)
        status = "✅" if os.path.exists(f_path) else "❌"
        print(f"   {status} {f}")
