import sqlite3

db = sqlite3.connect("database.db")

db.execute("""
CREATE TABLE IF NOT EXISTS achievements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT,
    achievement TEXT
)
""")

db.commit()

print("Achievement table created")
