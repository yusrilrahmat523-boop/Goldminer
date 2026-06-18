from database import get_db

db = get_db()

rows = db.execute(
    "SELECT * FROM users"
).fetchall()

print("Jumlah user:", len(rows))

for row in rows:
    print(dict(row))
