from database import get_db

db = get_db()

try:
    db.execute(
        "ALTER TABLE users ADD COLUMN speed INTEGER DEFAULT 5"
    )

    db.commit()

    print("Kolom speed berhasil ditambah")

except Exception as e:

    print("Mungkin kolom sudah ada:", e)
