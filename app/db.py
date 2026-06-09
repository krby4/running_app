import sqlite3
import pathlib
import os

# make directory if it doesn't exist
BASE_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_DB_PATH = pathlib.Path(os.environ.get("RUNNING_DB_PATH", str(BASE_DIR.parent / "data" / "running.db"))) 
def get_connection(db_path=None):
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    db_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

if __name__ == "__main__":
    conn = get_connection()
    print(f"Connected to {DEFAULT_DB_PATH}")
    conn.close()