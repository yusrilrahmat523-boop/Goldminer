from database import get_db

db = get_db()

db.execute("""
INSERT INTO users
(id,gold,power)

VALUES

(1,0,1)
""")

db.commit()

print("User dibuat")
