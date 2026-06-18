alert("APP JS LOADED");

const tg = window.Telegram?.WebApp;

let user = null;

if (tg) {

    tg.expand();

    user = tg.initDataUnsafe?.user;

    console.log("Telegram User:", user);

} else {

    console.log(
        "Telegram SDK tidak ditemukan"
    );

}

let gold = 0;
let power = 1;
let referralLink = "";

let autoMineInterval = null;

const goldText = document.getElementById("gold");
const powerText = document.getElementById("power");
const leaderboardText =
document.getElementById("leaderboard");
const referralInfoText =
document.getElementById(
    "referralInfo"
);
const playerStatsText =
document.getElementById(
    "playerStats"
);
const questInfoText =
document.getElementById(
    "questInfo"
);
const shopItemsText =
document.getElementById(
    "shopItems"
);

const inventoryListText =
document.getElementById(
    "inventoryList"
);

const achievementListText =
document.getElementById(
    "achievementList"
);

const wheelInfoText =
document.getElementById(
    "wheelInfo"
);

const streakInfoText =
document.getElementById(
    "streakInfo"
);

const telegramUserInfo =
document.getElementById(
    "telegramUserInfo"
);

console.log("telegramUserInfo:", telegramUserInfo);
console.log("user:", user);

/*
========================
LOAD PROFILE
========================
*/

async function loadProfile() {

    const res = await fetch("/api/profile");
    const data = await res.json();

    gold = data.gold;
    power = data.power;
    speed = data.speed;

    render();

    startAutoMine();
}

/*
========================
UPDATE TAMPILAN
========================
*/

function render() {

    goldText.innerHTML = gold;

    powerText.innerHTML =
        "Power: " + power;
}

/*
========================
MANUAL MINE
========================
*/

async function mine() {

    const res = await fetch(
        "/api/mine",
        {
            method: "POST"
        }
    );

    const data = await res.json();

    gold = data.gold;
    power = data.power;

    render();
}

/*
========================
UPGRADE POWER
========================
*/

async function upgrade() {

    const res = await fetch(
        "/api/upgrade",
        {
            method: "POST"
        }
    );

    const data = await res.json();

    if (!data.success) {

        alert(data.message);
        return;
    }

    gold = data.gold;
    power = data.power;

    render();
}

/*
========================
AUTO MINE
========================
*/

async function autoMine() {

    const res = await fetch(
        "/api/auto_mine",
        {
            method: "POST"
        }
    );

    const data = await res.json();

    gold = data.gold;
    power = data.power;

    render();
}

/*
========================
DAILY REWARD
========================
*/

async function dailyReward() {

    const res = await fetch(
        "/api/daily_reward",
        {
            method: "POST"
        }
    );

    const data = await res.json();

    if (!data.success) {

        alert(data.message);
        return;
    }

    gold = data.gold;

    render();

    alert(
        "Reward +" +
        data.reward +
        " Gold"
    );
}

/*
========================
REFERRAL CLAIM
========================
*/

async function referralClaim() {

    const res = await fetch(
        "/api/referral_claim",
        {
            method: "POST"
        }
    );

    const data = await res.json();

    if (!data.success) {

        alert(data.message);
        return;
    }

    alert(
        "Referral +" +
        data.reward +
        " Gold"
    );

    loadProfile();
    loadLeaderboard();
    loadReferralInfo();
}

/*
========================
LEADERERBOARD
========================
*/

async function loadLeaderboard() {

    const res = await fetch(
        "/api/leaderboard"
    );

    const data = await res.json();

    let html = "";

    let rank = 1;

    data.forEach(player => {

        html +=
            rank +
            ". " +
            player.username +
            " - " +
            player.gold +
            "<br>";

        rank++;

    });

    leaderboardText.innerHTML =
        html;
}

/*
========================
REFERRAL INFO
========================
*/

async function loadReferralInfo() {

    const res = await fetch(
        "/api/referral_info"
    );

    const data = await res.json();

    referralLink =
        "https://t.me/GoldMinerBot?start=" +
        data.telegram_id;

    referralInfoText.innerHTML =
        `
        <b>Username:</b> ${data.username}
        <br><br>

        <b>Referral ID:</b> ${data.telegram_id}
        <br><br>

        <b>Total Referral:</b> ${data.total_referrals}
        <br><br>

        <b>Bonus/User:</b> ${data.referral_bonus} Gold
        <br><br>

        <b>Link Referral:</b>
        <br>
        ${referralLink}
        `;
}

async function loadPlayerStats() {

    const res = await fetch(
        "/api/player_stats"
    );

    const data = await res.json();

    playerStatsText.innerHTML =
        `
        <b>Username:</b>
        ${data.username}

        <br><br>

        <b>Gold:</b>
        ${data.gold}

        <br><br>

        <b>Level:</b>
        ⭐ ${data.level}

        <br><br>

        <b>Power:</b>
        ${data.power}

        <br><br>

        <b>Speed:</b>
        ${data.speed} sec

        <br><br>

        <b>Rank:</b>
        #${data.rank}

        <br><br>

        <b>Referral:</b>
        ${data.referrals}

        <br><br>

        <b>Prestige:</b>
        ⭐ ${data.prestige}
        `;
}

async function loadQuestInfo() {

    const res =
    await fetch(
        "/api/quest_info"
    );

    const data =
    await res.json();

    let status =
    data.claimed
        ? "✅ Selesai"
        : "⌛ Belum Diklaim";

    questInfoText.innerHTML =
        `
        <b>Target:</b>
        ${data.goal} Gold

        <br><br>

        <b>Reward:</b>
        ${data.reward} Gold

        <br><br>

        <b>Progress:</b>
        ${data.gold}/${data.goal}

        <br><br>

        <b>Status:</b>
        ${status}
        `;
}

async function claimQuest() {

    const res =
    await fetch(
        "/api/claim_quest",
        {
            method:"POST"
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        "🎁 Quest Reward +" +
        data.reward +
        " Gold"
    );

    loadProfile();

    loadPlayerStats();

    loadQuestInfo();

    loadLeaderboard();
}

/*
========================
COPY REFERRAL LINK
========================
*/

function copyReferralLink() {

    navigator.clipboard.writeText(
        referralLink
    );

    alert(
        "Link referral berhasil disalin"
    );
}

async function loadShop() {

    const res =
    await fetch(
        "/api/shop"
    );

    const items =
    await res.json();

    let html = "";

    items.forEach(item => {

        html += `
        <div style="
            border:1px solid #555;
            padding:10px;
            margin:10px;
        ">

            <b>${item.name}</b>

            <br><br>

            Harga:
            ${item.price} Gold

            <br><br>

            Bonus:
            +${item.power} Power

            <br><br>

            <button
                onclick="buyItem('${item.name}')"
            >
                Beli
            </button>

        </div>
        `;
    });

    shopItemsText.innerHTML =
        html;
}

async function buyItem(itemName) {

    const res =
    await fetch(
        "/api/buy_item",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                item: itemName
            })
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        itemName +
        " berhasil dibeli"
    );

    loadProfile();

    loadPlayerStats();

    loadLeaderboard();

    loadInventory();
}

async function loadInventory() {

    const res =
    await fetch(
        "/api/inventory"
    );

    const items =
    await res.json();

    if(items.length === 0){

        inventoryListText.innerHTML =
        "Belum ada item";

        return;
    }

    let html = "";

    items.forEach(item => {

        html +=
        "🎁 " +
        item +
        "<br>";
    });

    inventoryListText.innerHTML =
        html;
}

async function loadAchievements() {

    const res =
    await fetch(
        "/api/achievements"
    );

    const data =
    await res.json();

    if(data.length === 0){

        achievementListText.innerHTML =
        "Belum ada achievement";

        return;
    }

    let html = "";

    data.forEach(item => {

        let status = "";

        if(item.claimed){

            status =
            "✅ Sudah Diklaim";

        }else{

            status =
            `
            <button
            onclick="claimAchievement(
            '${item.achievement}'
            )">
            🎁 Claim Reward
            </button>
            `;
        }

        html +=
        `
        <div style="
        border:1px solid #555;
        margin:10px;
        padding:10px;
        ">

        <b>
        🏆 ${item.achievement}
        </b>

        <br><br>

        Reward:
        ${item.reward} Gold

        <br><br>

        ${status}

        </div>
        `;
    });

    achievementListText.innerHTML =
    html;
}

async function claimAchievement(
    achievement
){

    const res =
    await fetch(
        "/api/claim_achievement",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                achievement:
                achievement
            })
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        "🎉 Reward +" +
        data.reward +
        " Gold"
    );

    loadProfile();

    loadPlayerStats();

    loadAchievements();
}

function startAutoMine() {

    if(autoMineInterval){

        clearInterval(
            autoMineInterval
        );
    }

    autoMineInterval =
    setInterval(
        autoMine,
        speed * 1000
    );
}

async function upgradeSpeed() {

    const res =
    await fetch(
        "/api/upgrade_speed",
        {
            method:"POST"
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        "⚡ Speed naik menjadi " +
        data.speed
    );

    loadProfile();

    loadPlayerStats();
}

async function loadWheelInfo() {

    const res =
    await fetch(
        "/api/wheel_info"
    );

    const data =
    await res.json();

    const hours =
    Math.floor(
        data.remaining / 3600
    );

    const minutes =
    Math.floor(
        (data.remaining % 3600)
        / 60
    );

    wheelInfoText.innerHTML =
    `
    <b>Cooldown:</b>
    ${hours} jam ${minutes} menit
    `;
}

async function spinWheel() {

    const res =
    await fetch(
        "/api/spin_wheel",
        {
            method:"POST"
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        "🎉 Hadiah: " +
        data.reward_value +
        " " +
        data.reward_type
    );

    loadProfile();
    loadPlayerStats();
    loadWheelInfo();
}

async function loadStreakInfo() {

    const res =
    await fetch(
        "/api/streak_info"
    );

    const data =
    await res.json();

    streakInfoText.innerHTML =
    `
    <b>Hari Ke:</b>
    ${data.streak_day}
    `;
}

async function claimStreak() {

    const res =
    await fetch(
        "/api/claim_streak",
        {
            method:"POST"
        }
    );

    const data =
    await res.json();

    if(!data.success){

        alert(
            data.message
        );

        return;
    }

    alert(
        "🔥 Hari " +
        data.day +
        " Reward +" +
        data.reward +
        " Gold"
    );

    loadProfile();
    loadPlayerStats();
    loadStreakInfo();
}

/*
========================
BUTTON EVENTS
========================
*/

document
.getElementById("mineBtn")
.addEventListener(
    "click",
    mine
);

document
.getElementById("upgradeBtn")
.addEventListener(
    "click",
    upgrade
);

document
.getElementById("dailyBtn")
.addEventListener(
    "click",
    dailyReward
);

document
.getElementById("referralBtn")
.addEventListener(
    "click",
    referralClaim
);

document
.getElementById("copyReferralBtn")
.addEventListener(
    "click",
    copyReferralLink
);

document
.getElementById(
    "claimQuestBtn"
)
.addEventListener(
    "click",
    claimQuest
);

document
.getElementById("speedBtn")
.addEventListener(
    "click",
    upgradeSpeed
);

document
.getElementById(
    "spinWheelBtn"
)
.addEventListener(
    "click",
    spinWheel
);

document
.getElementById(
    "claimStreakBtn"
)
.addEventListener(
    "click",
    claimStreak
);

console.log("Panel Telegram dijalankan");

if (user) {

    telegramUserInfo.innerHTML =
    `
    <b>ID:</b>
    ${user.id}

    <br><br>

    <b>Username:</b>
    ${user.username || "-"}

    <br><br>

    <b>Nama:</b>
    ${user.first_name}
    `;

} else {

    telegramUserInfo.innerHTML =
    "Telegram User Tidak Terdeteksi";

}

/*
========================
START GAME
========================
*/

telegramUserInfo.innerHTML =
"TEST BERHASIL";

loadProfile();

loadLeaderboard();

loadReferralInfo();

loadPlayerStats();

loadQuestInfo();

loadShop();

loadInventory();

loadAchievements();

loadWheelInfo();

loadStreakInfo();

setInterval(
    loadLeaderboard,
    10000
);

setInterval(
    loadReferralInfo,
    10000
);

setInterval(
    loadPlayerStats,
    10000
);

setInterval(
    loadQuestInfo,
    10000
);

setInterval(
    loadAchievements,
    10000
);

setInterval(
    loadWheelInfo,
    10000
);

setInterval(
    loadStreakInfo,
    10000
);
