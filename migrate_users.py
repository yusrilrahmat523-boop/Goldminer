from database import get_db

db = get_db()

try:

    db.execute(
        "ALTER TABLE users ADD COLUMN telegram_id TEXT"
    )

    db.commit()

    print("telegram_id berhasil ditambah")

except Exception as e:

    print(e)

try:

    db.execute(
        "ALTER TABLE users ADD COLUMN username TEXT"
    )

    db.commit()

    print("username berhasil ditambah")

except Exception as e:

    print(e)
