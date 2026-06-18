from database import get_db

db = get_db()

try:

    db.execute(
        """
        ALTER TABLE users
        ADD COLUMN referral_claimed INTEGER DEFAULT 0
        """
    )

    db.commit()

    print("Kolom referral_claimed dibuat")

except Exception as e:

    print(e)
