from database import get_db

db = get_db()

db.execute(
    """
    UPDATE users
    SET telegram_id=?
    WHERE id=2
    """,
    ("987654321",)
)

db.commit()

print("User diperbaiki")
