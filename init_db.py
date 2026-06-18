from database import get_db

db = get_db()

db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    gold INTEGER DEFAULT 0,
    power INTEGER DEFAULT 1
)
""")

db.commit()

print("Database berhasil dibuat")
