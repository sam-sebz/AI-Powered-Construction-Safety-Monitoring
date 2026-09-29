import sqlite3
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"data"/"ppe_monitoring.db"
SCHEMA=ROOT/"database"/"schema.sql"

def conn():
    DB.parent.mkdir(exist_ok=True)
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.executescript(SCHEMA.read_text())

def add_incident(event_type,severity,description,compliance=None,source="api"):
    now=datetime.now(timezone.utc).isoformat()
    with conn() as c:
        cur=c.execute(
            "INSERT INTO incidents(event_type,severity,description,compliance,source,created_at) VALUES(?,?,?,?,?,?)",
            (event_type,severity,description,compliance,source,now))
        c.commit()
        return cur.lastrowid

def list_incidents(limit=50):
    with conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM incidents ORDER BY id DESC LIMIT ?",(limit,)).fetchall()]
