CREATE TABLE IF NOT EXISTS incidents (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 event_type TEXT NOT NULL,
 severity TEXT NOT NULL,
 description TEXT NOT NULL,
 compliance INTEGER,
 source TEXT NOT NULL,
 created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_metrics (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 metric_name TEXT NOT NULL,
 metric_value REAL NOT NULL,
 evaluation_set TEXT NOT NULL,
 created_at TEXT NOT NULL
);
