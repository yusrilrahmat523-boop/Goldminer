from database import get_db

db = get_db()

try:

    db.execute(
        "ALTER TABLE users ADD COLUMN daily_claimed INTEGER DEFAULT 0"
    )

    db.commit()

    print("Kolom daily_claimed berhasil dibuat")

except Exception as e:

    print("Kemungkinan kolom sudah ada")
    print(e)
