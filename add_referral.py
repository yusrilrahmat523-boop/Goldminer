from database import get_db

db = get_db()

try:

    db.execute(
        """
        ALTER TABLE users
        ADD COLUMN referrer TEXT
        """
    )

    db.commit()

    print("Kolom referrer dibuat")

except Exception as e:

    print(e)
