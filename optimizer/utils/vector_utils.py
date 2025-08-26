import os
import shutil


def is_valid_chroma_vector_db(path: str) -> bool:
    """Check if a directory looks like a valid Chroma vector DB."""
    if not os.path.exists(path):
        return False

    # Check for chroma.sqlite3 file (modern ChromaDB format)
    sqlite_file = os.path.join(path, "chroma.sqlite3")
    if os.path.exists(sqlite_file):
        return True

    # Check for legacy parquet files format
    legacy_files = [
        "chroma-collections.parquet",
        "chroma-embeddings.parquet",
        "index",
        "chroma-lock",
    ]
    return all(os.path.exists(os.path.join(path, f)) for f in legacy_files)


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

    # Check modern format
    sqlite_file = os.path.join(path, "chroma.sqlite3")
    status = "✅" if os.path.exists(sqlite_file) else "❌"
    print(f"   {status} chroma.sqlite3")

    # Check legacy format
    legacy_files = [
        "chroma-collections.parquet",
        "chroma-embeddings.parquet",
        "index",
        "chroma-lock",
    ]
    for f in legacy_files:
        f_path = os.path.join(path, f)
        status = "✅" if os.path.exists(f_path) else "❌"
        print(f"   {status} {f}")
