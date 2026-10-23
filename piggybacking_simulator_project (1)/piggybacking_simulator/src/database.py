import sqlite3
from pathlib import Path
from datetime import datetime

DB = Path("piggybacking.db")

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS simulation_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            a_to_b INTEGER,
            b_to_a INTEGER,
            normal_frames INTEGER,
            piggy_frames INTEGER,
            frames_saved INTEGER,
            bandwidth_saved_pct REAL
        )
        """)

def save_run(result):
    p = result["parameters"]
    c = result["comparison"]
    with sqlite3.connect(DB) as con:
        con.execute("""
        INSERT INTO simulation_runs
        (created_at, a_to_b, b_to_a, normal_frames, piggy_frames, frames_saved, bandwidth_saved_pct)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(timespec="seconds"),
            p["a_to_b"], p["b_to_a"],
            result["normal"]["total_frames"],
            result["piggyback"]["total_frames"],
            c["frames_saved"],
            c["bandwidth_saved_pct"]
        ))

def load_runs():
    with sqlite3.connect(DB) as con:
        cur = con.execute("""
        SELECT id, created_at, a_to_b, b_to_a, normal_frames,
               piggy_frames, frames_saved, ROUND(bandwidth_saved_pct, 2)
        FROM simulation_runs ORDER BY id DESC LIMIT 20
        """)
        rows = cur.fetchall()
    columns = ["ID", "Created", "A→B", "B→A", "Normal Frames",
               "Piggyback Frames", "Frames Saved", "Bandwidth Saved %"]
    return [dict(zip(columns, r)) for r in rows]
