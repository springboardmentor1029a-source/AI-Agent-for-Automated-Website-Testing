import sqlite3, json

def init_db():
    with sqlite3.connect("history.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instruction TEXT,
                target TEXT,
                mode TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_run_history(instruction, target, mode, result):
    with sqlite3.connect("history.db") as conn:
        conn.execute(
            "INSERT INTO history (instruction, target, mode, result) VALUES (?, ?, ?, ?)",
            (instruction, target, mode, json.dumps(result))
        )

def get_run_history(limit=10):
    with sqlite3.connect("history.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

        return [{
            "instruction": r["instruction"],
            "target": r["target"],
            "mode": r["mode"],
            "full_report": json.loads(r["result"]),
            "timestamp": r["timestamp"]
        } for r in rows]
