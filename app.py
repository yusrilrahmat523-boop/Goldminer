import sqlite3
import time
import random

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from datetime import date

from database import get_db

app = Flask(__name__)

# ==========================================
# TEST USER
# ==========================================

TEST_TELEGRAM_ID = "987654321"

# ==========================================
# HELPER
# ==========================================

def get_user():

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id=?
        """,
        (
            TEST_TELEGRAM_ID,
        )
    ).fetchone()

    return user


def calculate_level(gold):

    if gold >= 5000:
        return 5

    elif gold >= 1000:
        return 4

    elif gold >= 500:
        return 3

    elif gold >= 100:
        return 2

    else:
        return 1

def check_achievements(user):

    db = get_db()

    gold = user["gold"]

    achievements = db.execute(
        """
        SELECT achievement
        FROM achievements
        WHERE telegram_id=?
        """,
        (
            user["telegram_id"],
        )
    ).fetchall()

    owned = []

    for a in achievements:

        owned.append(
            a["achievement"]
        )

    if gold >= 100 and "First Gold" not in owned:

        db.execute(
            """
            INSERT INTO achievements(
                telegram_id,
                achievement
            )
            VALUES(?,?)
            """,
            (
                user["telegram_id"],
                "First Gold"
            )
        )

    if gold >= 500 and "Rich Miner" not in owned:

        db.execute(
            """
            INSERT INTO achievements(
                telegram_id,
                achievement
            )
            VALUES(?,?)
            """,
            (
                user["telegram_id"],
                "Rich Miner"
            )
        )

    if gold >= 1000 and "Gold Master" not in owned:

        db.execute(
            """
            INSERT INTO achievements(
                telegram_id,
                achievement
            )
            VALUES(?,?)
            """,
            (
                user["telegram_id"],
                "Gold Master"
            )
        )

    db.commit()

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ==========================================
# PROFILE
# ==========================================

@app.route("/api/profile")
def profile():

    user = get_user()

    return jsonify({
    "gold": user["gold"],
    "power": user["power"],
    "prestige": user["prestige"],
    "speed": user["speed"]
 })

# ==========================================
# MANUAL MINE
# ==========================================

@app.route(
    "/api/mine",
    methods=["POST"]
)
def mine():

    db = get_db()

    user = get_user()

    gold = user["gold"]
    power = user["power"]

    bonus = 1 + (
    user["prestige"] * 0.1
    )

    gold += int(
    power * bonus
    )

    db.execute(
        """
        UPDATE users
        SET gold=?
        WHERE telegram_id=?
        """,
        (
            gold,
            TEST_TELEGRAM_ID
        )
    )

    db.commit()

    user = get_user()

    check_achievements(user)

    return jsonify({
        "gold": gold,
        "power": power
    })

# ==========================================
# UPGRADE POWER
# ==========================================

@app.route(
    "/api/upgrade",
    methods=["POST"]
)
def upgrade():

    db = get_db()

    user = get_user()

    gold = user["gold"]
    power = user["power"]

    cost = power * 10

    if gold < cost:

        return jsonify({
            "success": False,
            "message": "Gold tidak cukup"
        })

    gold -= cost
    power += 1

    db.execute(
        """
        UPDATE users
        SET gold=?,
            power=?
        WHERE telegram_id=?
        """,
        (
            gold,
            power,
            TEST_TELEGRAM_ID
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": gold,
        "power": power
    })

# ==========================================
# AUTO MINE
# ==========================================

@app.route(
    "/api/auto_mine",
    methods=["POST"]
)
def auto_mine():

    db = get_db()

    user = get_user()

    gold = user["gold"]
    power = user["power"]

    bonus = 1 + (
    user["prestige"] * 0.1
    )

    gold += int(
    power * bonus
    )

    db.execute(
        """
        UPDATE users
        SET gold=?
        WHERE telegram_id=?
        """,
        (
            gold,
            TEST_TELEGRAM_ID
        )
    )

    db.commit()

    return jsonify({
        "gold": gold,
        "power": power
    })

# ==========================================
# DAILY REWARD
# ==========================================

@app.route(
    "/api/daily_reward",
    methods=["POST"]
)
def daily_reward():

    db = get_db()

    user = get_user()

    if user["daily_claimed"] == 1:

        return jsonify({
            "success": False,
            "message": "Reward sudah diklaim"
        })

    reward = 100

    gold = (
        user["gold"]
        + reward
    )

    db.execute(
        """
        UPDATE users
        SET gold=?,
            daily_claimed=1
        WHERE telegram_id=?
        """,
        (
            gold,
            TEST_TELEGRAM_ID
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": gold,
        "reward": reward
    })

# ==========================================
# LEADERBOARD
# ==========================================

@app.route("/api/leaderboard")
def leaderboard():

    db = get_db()

    users = db.execute(
        """
        SELECT username,
               gold
        FROM users
        ORDER BY gold DESC
        LIMIT 10
        """
    ).fetchall()

    result = []

    for user in users:

        result.append({
            "username": user["username"],
            "gold": user["gold"]
        })

    return jsonify(result)

# ==========================================
# REFERRAL CLAIM
# ==========================================

@app.route(
    "/api/referral_claim",
    methods=["POST"]
)
def referral_claim():

    db = get_db()

    user = get_user()

    if user["referral_claimed"] == 1:

        return jsonify({
            "success": False,
            "message": "Referral sudah diklaim"
        })

    if not user["referrer"]:

        return jsonify({
            "success": False,
            "message": "Tidak ada referral"
        })

    referrer = db.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id=?
        """,
        (
            user["referrer"],
        )
    ).fetchone()

    if not referrer:

        return jsonify({
            "success": False,
            "message": "Referrer tidak ditemukan"
        })

    reward = 500

    new_gold = (
        referrer["gold"]
        + reward
    )

    db.execute(
        """
        UPDATE users
        SET gold=?
        WHERE telegram_id=?
        """,
        (
            new_gold,
            referrer["telegram_id"]
        )
    )

    db.execute(
        """
        UPDATE users
        SET referral_claimed=1
        WHERE telegram_id=?
        """,
        (
            user["telegram_id"],
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "reward": reward
    })

# ==========================================
# REFERRAL INFO
# ==========================================

@app.route("/api/referral_info")
def referral_info():

    db = get_db()

    user = get_user()

    total_referrals = db.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE referrer=?
        """,
        (
            user["telegram_id"],
        )
    ).fetchone()[0]

    return jsonify({
        "telegram_id": user["telegram_id"],
        "username": user["username"],
        "total_referrals": total_referrals,
        "referral_bonus": 500
    })

# ==========================================
# PLAYER STATS
# ==========================================

@app.route("/api/player_stats")
def player_stats():

    db = get_db()

    user = get_user()

    rank = db.execute(
        """
        SELECT COUNT(*) + 1
        FROM users
        WHERE gold > ?
        """,
        (
            user["gold"],
        )
    ).fetchone()[0]

    referrals = db.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE referrer=?
        """,
        (
            user["telegram_id"],
        )
    ).fetchone()[0]

    level = calculate_level(
    user["gold"]
    )

    return jsonify({
    "username": user["username"],
    "gold": user["gold"],
    "power": user["power"],
    "rank": rank,
    "referrals": referrals,
    "level": level,
    "prestige": user["prestige"],
    })

@app.route("/api/quest_info")
def quest_info():

    db = get_db()

    user = get_user()

    today = str(
        date.today()
    )

    if user["quest_date"] != today:

        db.execute(
            """
            UPDATE users
            SET quest_claimed=0,
                quest_date=?
            WHERE telegram_id=?
            """,
            (
                today,
                user["telegram_id"]
            )
        )

        db.commit()

        user = get_user()

    return jsonify({
        "goal": 20,
        "reward": 50,
        "gold": user["gold"],
        "claimed": user["quest_claimed"]
    })

@app.route("/api/claim_quest",
    methods=["POST"]
)
def claim_quest():

    db = get_db()

    user = get_user()

    if user["quest_claimed"] == 1:

        return jsonify({
            "success": False,
            "message": "Quest sudah diklaim"
        })

    if user["gold"] < 20:

        return jsonify({
            "success": False,
            "message": "Target belum tercapai"
        })

    gold = user["gold"] + 50

    db.execute(
    """
    UPDATE users
    SET gold=?,
        quest_claimed=1,
        quest_date=?
    WHERE telegram_id=?
    """,
    (
        gold,
        str(date.today()),
        user["telegram_id"]
    )
)

    db.commit()

    return jsonify({
        "success": True,
        "reward": 50,
        "gold": gold
    })

@app.route("/api/shop")
def shop():

    items = [

        {
            "name": "Drill",
            "price": 100,
            "power": 1
        },

        {
            "name": "Excavator",
            "price": 500,
            "power": 5
        },

        {
            "name": "Robot Miner",
            "price": 1000,
            "power": 10
        }

    ]

    return jsonify(items)

@app.route(
    "/api/buy_item",
    methods=["POST"]
)
def buy_item():

    db = get_db()

    user = get_user()

    data = request.get_json()

    item_name = data["item"]

    items = {

        "Drill": {
            "price": 100,
            "power": 1
        },

        "Excavator": {
            "price": 500,
            "power": 5
        },

        "Robot Miner": {
            "price": 1000,
            "power": 10
        }

    }

    if item_name not in items:

        return jsonify({
            "success": False,
            "message": "Item tidak ditemukan"
        })

    price = items[item_name]["price"]

    bonus = items[item_name]["power"]

    if user["gold"] < price:

        return jsonify({
            "success": False,
            "message": "Gold tidak cukup"
        })

    new_gold = user["gold"] - price

    new_power = user["power"] + bonus

    db.execute(
        """
        UPDATE users
        SET gold=?,
            power=?
        WHERE telegram_id=?
        """,
        (
            new_gold,
            new_power,
            user["telegram_id"]
        )
    )

    db.execute(
        """
        INSERT INTO inventory(
            telegram_id,
            item_name
        )
        VALUES(?,?)
        """,
        (
            user["telegram_id"],
            item_name
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": new_gold,
        "power": new_power
    })

@app.route("/api/inventory")
def inventory():

    db = get_db()

    user = get_user()

    items = db.execute(
        """
        SELECT item_name
        FROM inventory
        WHERE telegram_id=?
        """,
        (
            user["telegram_id"],
        )
    ).fetchall()

    result = []

    for item in items:

        result.append(
            item["item_name"]
        )

    return jsonify(result)

@app.route("/api/achievements")
def achievements():

    db = get_db()

    user = get_user()

    rows = db.execute(
        """
        SELECT *
        FROM achievements
        WHERE telegram_id=?
        """,
        (
            user["telegram_id"],
        )
    ).fetchall()

    result = []

    rewards = {

        "First Gold": 50,
        "Rich Miner": 100,
        "Gold Master": 250

    }

    for row in rows:

        result.append({

            "achievement":
            row["achievement"],

            "claimed":
            row["claimed"],

            "reward":
            rewards.get(
                row["achievement"],
                0
            )

        })

    return jsonify(result)

@app.route(
    "/api/claim_achievement",
    methods=["POST"]
)
def claim_achievement():

    db = get_db()

    user = get_user()

    data = request.get_json()

    achievement = data["achievement"]

    row = db.execute(
        """
        SELECT *
        FROM achievements
        WHERE telegram_id=?
        AND achievement=?
        """,
        (
            user["telegram_id"],
            achievement
        )
    ).fetchone()

    if not row:

        return jsonify({
            "success": False,
            "message": "Achievement tidak ditemukan"
        })

    if row["claimed"] == 1:

        return jsonify({
            "success": False,
            "message": "Reward sudah diklaim"
        })

    rewards = {
        "First Gold": 50,
        "Rich Miner": 100,
        "Gold Master": 250
    }

    reward = rewards.get(
        achievement,
        0
    )

    new_gold = user["gold"] + reward

    db.execute(
        """
        UPDATE users
        SET gold=?
        WHERE telegram_id=?
        """,
        (
            new_gold,
            user["telegram_id"]
        )
    )

    db.execute(
        """
        UPDATE achievements
        SET claimed=1
        WHERE id=?
        """,
        (
            row["id"],
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "reward": reward,
        "gold": new_gold
    })

@app.route(
    "/api/prestige",
    methods=["POST"]
)
def prestige():

    db = get_db()

    user = get_user()

    if user["gold"] < 5000:

        return jsonify({
            "success": False,
            "message": "Butuh 5000 Gold"
        })

    new_prestige = user["prestige"] + 1

    db.execute(
        """
        UPDATE users
        SET gold=?,
            power=?,
            prestige=?
        WHERE telegram_id=?
        """,
        (
            0,
            1,
            new_prestige,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "prestige": new_prestige
    })

@app.route(
    "/api/upgrade_speed",
    methods=["POST"]
)
def upgrade_speed():

    db = get_db()

    user = get_user()

    gold = user["gold"]
    speed = user["speed"]

    if speed <= 1:

        return jsonify({
            "success": False,
            "message": "Speed sudah maksimal"
        })

    cost = (6 - speed) * 200

    if gold < cost:

        return jsonify({
            "success": False,
            "message": "Gold tidak cukup"
        })

    gold -= cost
    speed -= 1

    db.execute(
        """
        UPDATE users
        SET gold=?,
            speed=?
        WHERE telegram_id=?
        """,
        (
            gold,
            speed,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": gold,
        "speed": speed
    })

@app.route("/api/bank_info")
def bank_info():

    user = get_user()

    return jsonify({
        "gold": user["gold"],
        "bank_gold": user["bank_gold"]
    })

@app.route(
    "/api/bank_deposit",
    methods=["POST"]
)
def bank_deposit():

    db = get_db()

    user = get_user()

    amount = 10

    if user["gold"] < amount:

        return jsonify({
            "success": False,
            "message": "Gold tidak cukup"
        })

    new_gold = user["gold"] - amount

    new_bank = user["bank_gold"] + amount

    db.execute(
        """
        UPDATE users
        SET gold=?,
            bank_gold=?
        WHERE telegram_id=?
        """,
        (
            new_gold,
            new_bank,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": new_gold,
        "bank_gold": new_bank
    })

@app.route(
    "/api/bank_withdraw",
    methods=["POST"]
)
def bank_withdraw():

    db = get_db()

    user = get_user()

    amount = user["bank_gold"]

    if amount <= 0:

        return jsonify({
            "success": False,
            "message": "Bank kosong"
        })

    new_gold = user["gold"] + amount

    db.execute(
        """
        UPDATE users
        SET gold=?,
            bank_gold=0
        WHERE telegram_id=?
        """,
        (
            new_gold,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "gold": new_gold,
        "withdraw": amount
    })

@app.route(
    "/api/bank_interest",
    methods=["POST"]
)
def bank_interest():

    db = get_db()

    user = get_user()

    now = int(time.time())

    last_interest = user["last_interest"]

    cooldown = 3600

    if now - last_interest < cooldown:

        remaining = (
            cooldown -
            (now - last_interest)
        )

        return jsonify({
            "success": False,
            "message":
            f"Tunggu {remaining} detik lagi"
        })

    bank_gold = user["bank_gold"]

    if bank_gold <= 0:

        return jsonify({
            "success": False,
            "message": "Bank kosong"
        })

    interest = int(
        bank_gold * 0.05
    )

    if interest < 1:

        interest = 1

    new_bank = (
        bank_gold +
        interest
    )

    db.execute(
        """
        UPDATE users
        SET bank_gold=?,
            last_interest=?
        WHERE telegram_id=?
        """,
        (
            new_bank,
            now,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "interest": interest,
        "bank_gold": new_bank
    })

@app.route(
    "/api/spin_wheel",
    methods=["POST"]
)
def spin_wheel():

    db = get_db()

    user = get_user()

    now = int(time.time())

    if now - user["last_wheel"] < 86400:

        remaining = (
            86400 -
            (now - user["last_wheel"])
        )

        return jsonify({
            "success": False,
            "message":
            f"Tunggu {remaining} detik lagi"
        })

    rewards = [
        ("gold", 10),
        ("gold", 50),
        ("gold", 100),
        ("gold", 200),
        ("power", 1),
        ("prestige", 1),
        ("nothing", 0)
    ]

    reward_type, reward_value = random.choice(
        rewards
    )

    gold = user["gold"]
    power = user["power"]
    prestige = user["prestige"]

    if reward_type == "gold":
        gold += reward_value

    elif reward_type == "power":
        power += reward_value

    elif reward_type == "prestige":
        prestige += reward_value

    db.execute(
        """
        UPDATE users
        SET gold=?,
            power=?,
            prestige=?,
            last_wheel=?
        WHERE telegram_id=?
        """,
        (
            gold,
            power,
            prestige,
            now,
            user["telegram_id"]
        )
    )

    db.commit()

    return jsonify({
        "success": True,
        "reward_type": reward_type,
        "reward_value": reward_value
    })

@app.route("/api/wheel_info")
def wheel_info():

    user = get_user()

    now = int(time.time())

    cooldown = 86400

    remaining = max(
        0,
        cooldown -
        (now - user["last_wheel"])
    )

    return jsonify({
        "remaining": remaining
    })

@app.route("/api/streak_info")
def streak_info():

    user = get_user()

    return jsonify({
        "streak_day":
     user["streak_day"]
    })

@app.route(
"/api/claim_streak",
methods=["POST"]
)
def claim_streak():

    db = get_db()

    user = get_user()

    now = int(time.time())

    if (
        now -
        user["last_streak"]
    ) < 86400:

        return jsonify({
            "success": False,
            "message": "Sudah claim hari ini"
        })

    streak_day = user["streak_day"] + 1

    if streak_day > 7:

        streak_day = 1

    rewards = {
        1: 50,
        2: 100,
        3: 150,
        4: 200,
        5: 300,
        6: 500,
        7: 1000
    }

    reward = rewards[streak_day]

    new_gold = user["gold"] + reward

    db.execute(
        """
        UPDATE users
        SET gold=?,
        streak_day=?,
        last_streak=?
    WHERE telegram_id=?
    """,
    (
        new_gold,
        streak_day,
        now,
        user["telegram_id"]
    )
)

    db.commit()

    return jsonify({
        "success": True,
        "day": streak_day,
        "reward": reward,
        "gold": new_gold
})

# ==========================================
# START FLASK
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
