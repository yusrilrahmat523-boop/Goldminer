import sqlite3

db = sqlite3.connect("database.db")

try:
    db.execute("""
    ALTER TABLE users
    ADD COLUMN quest_claimed INTEGER DEFAULT 0
    """)

    print("quest_claimed berhasil ditambahkan")

except Exception as e:

    print(e)

db.commit()
db.close()
