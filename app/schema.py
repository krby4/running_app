from db import get_connection

def create_schema():
    conn = get_connection()

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY,
        user_id TEXT NOT NULL,
        run_date TEXT NOT NULL,
        run_type TEXT,
        start_time TEXT,
        end_time TEXT,
        duration_minutes REAL,
        distance_miles REAL,
        ave_hr INTEGER,
        max_hr INTEGER,
        rpe INTEGER,
        notes TEXT 
    );
    CREATE TABLE IF NOT EXISTS raw_run_takeout_data (
        id INTEGER PRIMARY KEY,
        run_date TEXT NOT NULL,
        body TEXT NOT NULL
    );                    

    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schema()
    print("Schema created")