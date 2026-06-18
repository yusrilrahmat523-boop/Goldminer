from database import get_db

db = get_db()

db.execute(
    """
    UPDATE users
    SET telegram_id=?,
        username=?
    WHERE id=1
    """,
    (
        "123456789",
        "admin"
    )
)

db.commit()

print("User diupdate")
