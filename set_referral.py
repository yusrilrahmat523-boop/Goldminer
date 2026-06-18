from database import get_db

db = get_db()

db.execute(
    """
    UPDATE users
    SET referrer=?
    WHERE telegram_id=?
    """,
    (
        "123456789",
        "987654321"
    )
)

db.commit()

print("Referral disimpan")
