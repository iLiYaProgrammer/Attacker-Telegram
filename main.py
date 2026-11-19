import asyncio
import random
from pathlib import Path

from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import (
    UserAlreadyParticipantError,
    InviteHashInvalidError,
    InviteHashExpiredError,
    FloodWaitError,
)

API_ID = 12345678
API_HASH = "You-Api-Hash"

ACCOUNT_COUNT = 10
DELAY = 0.1
SPAM_DELAY = 0.1
STAGGER_MAX = 0.15  # حداکثر تاخیر تصادفی بین اکانت‌ها در هر دور اسپم

SESSION_DIR = Path("session")
SESSION_DIR.mkdir(exist_ok=True)

SETTINGS_FILE = Path("settings.txt")
ADMINS_FILE = Path("admins.txt")
ENEMY_FILE = Path("enemies.txt")
FOSH_FILE = Path("fosh.txt")

DEFAULT_FOSH = [
    "ماشین با سرعت ۲۲۰ تا تو کس ننت",
    "خار کص مکانیکی",
    "تخمامو رو صورت ننت بمالم گریس ممبرک",
    "کیر پوگبا تو کس مادرت",
    "میگن گرگا قبل از اینکه بیان شیر مادرتو میخورن و گله میان",
    "تاج کیرم سنگینه مواظب باش میندازی سر مادرت گردنش نشکنه",
    "زیر تخت مادرت صدای گوز ضبط شده میزارم مشتریای مادرتو فراری میدم خودم صف اول شم",
    "عضو نیروی دلتای آمریکا میشم مادرتو درحال سکس با دوست پسرش با جاش میدزدم",
    "غیرت پدرت پینگش بالاس هی از سرور ناموست کانکت و دیسکانکت میشه",
    "آبجی کوچیکتو گاییدم",
    "تورک میشم به کسمادرت جفتک میزنم",
    "لر محلتون میشم با تمام قوا کسمادرت رو با سیمان آب بندی میکنم که دیگه حامله نشه",
    "بالا باش ناموص کیر دزد",
    "کیرم تو مادرت یخ زد باید اتیلن گلیکول بریزم.",
    "ننتو دادم ب دارکای افریقا گاییدن",
    "معترض میشم میشینم رو خیابون تا ننتو ندی بکنم پا نمیشم",
    "تو این دنیا 8,239,867,952 آدم وجود داره همونجوری که به تعداد توجه نکردی به اینکه قراره برینم دهن مادرت هم توجه نکن",
    "ناوگان بزرگی از کیر به سمت مادرت درحال حرکته.",
    "🛑پیام خامنه ای: کژمادرت",
    "ناوگان کشتی حامل بکن های مادرت به لنگرگاه‌ رسیده و فردا بدنبال ناموست صف می‌شوند",
    "خاله خارکونی خفه",
    "کیرم تو کفن مردهات بالا باش",
    "مرده کونی بالا باش",
    "ننه موس تخم نکن",
    "مادرت بردم پشت باغ گاییدم حاصلش تو بودی",
    "دالگ پیکنیکی",
    "خفه ناموص کونی ولدزنا",
    "ننه دولتی ",
    "ناموص کیردزد بالا باش",
    "کیر گروهبان آمریکا تو کص مص ننن تو کص ننت",
    "مادرت رو تمام اعضای خانواده قاطی میکنم و بعد میریزم تو مخزن تو قاطی میکنم",
    "از مامانت پرسیدن کیر چندتا حرف داره گفت کیر که حرف نداره",
    "پاهای مادرت رو مثل سگی که استخون دیده لیس میزنم",
    "مادر جنده ولد زنا ناموس کصته تو میخوای با من ابر انسان کل بندازی ننت میبرم زیر کیرم میکشم ننه خر حرومزاده",
    "من خدام مادرجنده فراریت میدم کونی ناموص",
    "شاشیدم رو صورت ناموصت",
    "بدو زجه بزن مث مامان جندت",
    "ننه مرده کونی",
    "دستم رو کص ناموصت",
    "بالا باش ناموص کونی از کص مادرت دفاع کن",
    "ساک بزن برام مثل مادرت",
    "شاش تو کص ننت",
    "و اما مادر جندت",
    "با تلمبه فاضلاب معده مادرتو از کصش دراوردم",
    "استین کوتاه تو کس ناموست",
    "مادرت بمیره فراری شو",
    "هورمون ترس ولاد رو از طریق نمونه های RNA کپی میکنم و به پدرت منتقل میکنم تا پدرت ترسو بشه و نتونه از مادرت دفاعی بکنه",
    "با مادرت تو کاسه توالت کمپین حمایت از گوه ها زدیم",
    "بدو بینم کیرم تو کصا خونتون",
    "با مسلسل گاتلینگ ۷ لول gau-8 avenger با نرخ آتش ۳۹۰۰ شلیک در دقیقه متعلق به هواپیمای پشتیبانی نزدیک a-10 thunderbolt II مواضع مادرت رو به گلوله میبندم",
    "کص مادرت رو کیرم بالا پایین میره بعدش مادرت میاد خایه هامو میخوره و مادرت با کونش خایه هامو ماساژ میده",
    "دارم از معدن کس مادرت فلز چوچولیوم استخراج میکنم",
    "وقتی میرفتم مادرتو زیر کیرم بگام چه حسی پیدا میکردی ؟",
    "گردن خارتو بخورم حشری شه؟",
    "عره برقی تو کس ننت😂",
    "برج میلاد تو کص ناموصت (از پهنا)",
    "موکت تو کس ناموست",
    "کصمادر کصممبرت",
    "انگشت پای چپ ملخ تو کون ننت",
    "فوری فوری فوری فوری                                     فاکس نیوز : مادرت بعد از ۸۰۰ساعت سکس مداوم با افراد نامعلوم هنوز به من کص نداده",
    "شب میام تو کابوس ناموست کیر می‌کنم تو ناموست",
    " مکش رحم مادرتو با گرون ترین جارو برقی بازار مقایسه کردم آپلود کردم یوتیوب شورت",
    "ننت تو جنده خونس برو جمش کن",
    " مامان کیر پرستت هر روز بهم اس ام اسای عاشقانه و احساسی میده ولی من با استیکر بادمجون خرش میکنم و میبرمش تو تختی که به بابات میده هر روز میکنمش",
    "ننتو میدم علی آلت زاده بگاد دیگه شاخ نشی بیناموص",
    "کص مادرت روم ریپ کنی",
    "انگور خوردم چاییدم زن آقاتو گاییدم",
    "شاش تو کص ناموصت",
    "کص مادرت چت بدی بدون نقض ",
    "مامانت با کونش کیرمو ماساژ میداد بعد سکس ",
    "ننه جندتو جلو بابای بی غیرتت گاییدم",
    "مادرت از پکیج های هکینگ تلگرام با ابزار ترموکس  همراه با کوروش سنایی ۶۰ درصد تخفیف گوه تره",
    "اونقدر که کص مادرتو انگشت کردم این نات کوینه رو نکردم",
    "مادرت مثل همستره همه انگشتش میکنن",
    "ماشاالله مادرش خیلی گشاده 54 تا کیر رفته توش ولی بازم جا داره",
    "مادرتو زیر کیرم شهید کردم الان خانواده شهید حساب میشی برو ذوق کن",
    "ننه کونی زمانی که من مادرجنده هایی مثل تورو ننشونو شهید میکردم تو, تو روبیکا داشتی فیلم سوپرای ننتو میفروختی",
    "كير تو روح ناپاک خواهرت",
    "کاربرات چهار دهنه نصب کردم روی مادرت الان میتونه ۴ تا کیرو همزمان بخوره",
    "شاید توهم قبلا مسئول بودی اخه این حجم از مادرجندگی تو انسانای عادی بعیده",
    "مادرت مال دولته‌ باید چاپید‌ قاپید",
    "واسه مامانت طلسم ناموس مگس گرفتم",
    "ناموس شفته گوه.",
    "با ذولفقاز‌ واسه مادرت خیار پوست کندم",
    "🔴ترامپ : یا با مادرت سر پول امشبش به توافق می‌رسیم، یا مجبوریم یه کار خیلی خشن بکنیم، مثل دفعه قبل. الان یه ناوگان کامل توی کسمادرته، شاید یکی دیگه هم در راه باشه.",
    "ارامگاه‌ مادرتو با گوه تِی کشیدم",
    "سیندرلا کفششو جاگذاشت مامان جندت شورتشو جا گذاشت خونمون",
    "خفه خارننه کونی ننه جیندرلا",
    "میشه مامانتو برام تیپاکس کنی لطفا؟",
    "ننت تو کون شاهزاده سرین",
    "ارّه برقی تو کون ناموصت",
    "کمد دیواری تو کص مادرت",
    "استخون مردهات تو کون زندهات ناموص کونی",
    "ناموص کونی تتپتپتتت نکن",
    "کصناموصت بالا باش یتیمت کنم",
    "از قدیم میگن با دم شیر بازی نکن میزنت الان میگن با دم من بازی نکن کیرمو در میارم میوفتم دنبال ننت",
    "با بیل و یه کلنگ میام تو کس مادرت یه چاله مرگ برای دشمنان ایران درست میکنم و هرکی قصد نزدکی به ایران رو داشت تو تله ای که تو کس مادرت درست کردم گیر میکنه و یواش یواش میمیره و حتی موشک های زمینی رو از سوراخ مادرت شلیک میکنم از سوراخ های بدن مادرت یه پایگاه جنگی درست میکنم میدونم موافقی ",
    "چقدر هوس گاییدن خاهرت تو فکرمه میدونی خاهرت اصلا قیافه میافه نداشت همش واسه منو رفقام ساک میزد و ما هم بهش نفری 50تومن میدادیم در واقع دلمون برای خاهرت میسوخت بقران حیف 50تومن بود خلاصه نگم برات که خاهرت این پولارو جمع کرد و رفت روی لباش ژل تزریق کرد و دماغشو که سه متر زود تر از خودش می اومد عمل کرد الان خودشو مریم مقدس میدونه جنده پولی!",
    "حیوون زبون نفهم عصبیم نکن این تکسای خزوخیل چیه میدی کیرم تو کفن پدرت کاری نکن با کلاش بی جواز بیام سراغ مادرت و ۳۰ تیر رو همزمان رگباری خالی کنم تو واژن بوگندو مادرت وقتی که مامانت مرد پزشک قانونی بگه به دلیل پارگی کس گشادش مرده و تو و اون داداشای بی غیرتت از دیه محروم بشید فکر کردی میزارم از جیبم سیر شین کیرممم نمیدم بخورین کس کثیف تموم مونث های خان��ادت",
    "ننه ۳تا کیر همزمان خورد هتریک کرد",
    "ناموص گراز راه فراری نیست اینجا خدا منم"
]

# ---------- FOSH ----------

def load_fosh():
    if FOSH_FILE.exists():
        try:
            lines = FOSH_FILE.read_text(encoding="utf-8").splitlines()
            result = [line for line in lines if line.strip()]
            if result:
                return result
            return DEFAULT_FOSH
        except Exception:
            return DEFAULT_FOSH
    else:
        save_fosh(DEFAULT_FOSH)
        return DEFAULT_FOSH

def save_fosh(fosh_list):
    try:
        FOSH_FILE.write_text("\n".join(fosh_list), encoding="utf-8")
    except Exception:
        pass

FOSH_LIST = load_fosh()

# ---------- CLIENTS ----------

accounts = []
for i in range(1, ACCOUNT_COUNT + 1):
    client = TelegramClient(str(SESSION_DIR / f"account{i}"), API_ID, API_HASH)
    accounts.append(client)

manager = TelegramClient(str(SESSION_DIR / "manager"), API_ID, API_HASH)

# ---------- STATE ----------

MANAGER_ID = None
SPAM_RUNNING = False
SPAM_MODE = None
REPLY_TARGETS = []
EXTRA_ADMINS = []
ENEMY_LIST = []

# ---------- SETTINGS ----------

def load_settings():
    global SPAM_DELAY
    if SETTINGS_FILE.exists():
        try:
            content = SETTINGS_FILE.read_text().strip()
            SPAM_DELAY = float(content)
        except Exception:
            pass

def save_settings():
    try:
        SETTINGS_FILE.write_text(str(SPAM_DELAY))
    except Exception:
        pass

def load_admins():
    global EXTRA_ADMINS
    if ADMINS_FILE.exists():
        try:
            lines = ADMINS_FILE.read_text().splitlines()
            EXTRA_ADMINS = []
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        EXTRA_ADMINS.append(int(line))
                    except Exception:
                        pass
        except Exception:
            EXTRA_ADMINS = []

def save_admins():
    try:
        ADMINS_FILE.write_text("\n".join(str(x) for x in EXTRA_ADMINS))
    except Exception:
        pass

def load_enemies():
    global ENEMY_LIST
    if ENEMY_FILE.exists():
        try:
            lines = ENEMY_FILE.read_text().splitlines()
            ENEMY_LIST = []
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        ENEMY_LIST.append(int(line))
                    except Exception:
                        pass
        except Exception:
            ENEMY_LIST = []

def save_enemies():
    try:
        ENEMY_FILE.write_text("\n".join(str(x) for x in ENEMY_LIST))
    except Exception:
        pass

# ---------- STARTUP ----------

async def login_manager():
    global MANAGER_ID
    await manager.start()
    me = await manager.get_me()
    MANAGER_ID = me.id
    print(f"Manager logged in: {me.id}")

async def load_accounts():
    for i, client in enumerate(accounts, 1):
        print(f"\n--- Checking Account {i} ---")
        try:
            await client.connect()
            if await client.is_user_authorized():
                me = await client.get_me()
                print(f"✅ Account {i}: ONLINE | {me.id}")
            else:
                print(f"❌ Account {i}: NOT LOGGED IN")
        except Exception as e:
            print(f"❌ Account {i}: ERROR | {e}")

# ---------- HELPERS ----------

async def admin_only(event):
    if event.sender_id == MANAGER_ID:
        return True
    if event.sender_id in EXTRA_ADMINS:
        return True
    return False

async def join_link(client, link):
    link = link.strip()
    if "t.me/+" in link:
        invite_hash = link.split("t.me/+", 1)[1].split("?", 1)[0]
        await client(ImportChatInviteRequest(invite_hash))
        return "joined"
    if "t.me/joinchat/" in link:
        invite_hash = link.split("t.me/joinchat/", 1)[1].split("?", 1)[0]
        await client(ImportChatInviteRequest(invite_hash))
        return "joined"
    username = link.rstrip("/").split("/")[-1]
    if username.startswith("@"):
        username = username[1:]
    await client(JoinChannelRequest(username))
    return "joined"

async def resolve_reply_target(chat_id):
    global REPLY_TARGETS
    if not REPLY_TARGETS:
        return None, []
    valid_targets = []
    for target in REPLY_TARGETS:
        try:
            msg = await manager.get_messages(chat_id, from_user=target["id"], limit=1)
            if msg:
                valid_targets.append({
                    "id": msg[0].id,
                    "user_id": target["id"],
                    "username": target["username"]
                })
        except Exception:
            pass
    tags = list(REPLY_TARGETS)
    if not valid_targets:
        return None, tags
    chosen = random.choice(valid_targets)
    return chosen["id"], tags

# ---------- ENEMY AUTO REPLY (روی همه اکانت‌ها) ----------

def make_enemy_handler(acc):
    async def handler(event):
        if not event.sender_id:
            return
        if event.sender_id not in ENEMY_LIST:
            return
        if not FOSH_LIST:
            return

        target_tag = f'<a href="tg://user?id={event.sender_id}">𒆙</a>'
        chat_id = event.chat_id
        reply_id = event.id

        async def reply_one(c):
            try:
                if not await c.is_user_authorized():
                    return
                await asyncio.sleep(random.uniform(0, STAGGER_MAX))
                await c.send_message(
                    chat_id,
                    f"{random.choice(FOSH_LIST)}\n\n{target_tag}",
                    reply_to=reply_id,
                    parse_mode="html"
                )
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                pass

        await asyncio.gather(*(reply_one(c) for c in accounts))
    return handler

for acc in accounts:
    acc.on(events.NewMessage(incoming=True))(make_enemy_handler(acc))

# ---------- MANAGER COMMANDS ----------

@manager.on(events.NewMessage(pattern=r"^list\s+fosh$"))
async def list_fosh_handler(event):
    if not await admin_only(event):
        return
    await event.reply(
        "**\n"
        f"📊 TOTAL FOSH: {len(FOSH_LIST)}\n"
        "**",
        parse_mode="markdown"
    )

@manager.on(events.NewMessage(pattern=r"^add\s+fosh\s+(.+)$"))
async def add_fosh_handler(event):
    global FOSH_LIST
    if not await admin_only(event):
        return
    new_fosh = event.pattern_match.group(1).strip()
    if new_fosh in FOSH_LIST:
        await event.reply("**\n⚠️ THIS FOSH ALREADY EXISTS.\n**", parse_mode="markdown")
        return
    FOSH_LIST.append(new_fosh)
    save_fosh(FOSH_LIST)
    await event.reply(
        "**\n"
        "✅ FOSH ADDED\n"
        f"📊 Total: {len(FOSH_LIST)}\n"
        "**",
        parse_mode="markdown"
    )

@manager.on(events.NewMessage(pattern=r"^remove\s+fosh\s+(.+)$"))
async def remove_fosh_handler(event):
    global FOSH_LIST
    if not await admin_only(event):
        return
    target_fosh = event.pattern_match.group(1).strip()
    if target_fosh in FOSH_LIST:
        FOSH_LIST.remove(target_fosh)
        save_fosh(FOSH_LIST)
        await event.reply(
            "**\n"
            "✅ FOSH REMOVED\n"
            f"📊 Total: {len(FOSH_LIST)}\n"
            "**",
            parse_mode="markdown"
        )
    else:
        await event.reply("**\n❌ FOSH NOT FOUND IN LIST.\n**", parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^setenemy$"))
async def set_enemy_handler(event):
    if not await admin_only(event):
        return
    if not event.is_reply:
        await event.reply("**\n⚠️ PLEASE REPLY TO A USER FIRST.\n**", parse_mode="markdown")
        return
    reply_msg = await event.get_reply_message()
    target_id = reply_msg.sender_id
    if target_id not in ENEMY_LIST:
        ENEMY_LIST.append(target_id)
        save_enemies()
        await event.reply("**\n✅ ENEMY ADDED\n**", parse_mode="markdown")
    else:
        await event.reply("**\nℹ️ USER IS ALREADY IN ENEMY LIST.\n**", parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^remove\s+enemy$"))
async def remove_enemy_handler(event):
    global ENEMY_LIST
    if not await admin_only(event):
        return
    if not event.is_reply:
        await event.reply("**\n⚠️ PLEASE REPLY TO A USER FIRST.\n**", parse_mode="markdown")
        return
    reply_msg = await event.get_reply_message()
    target_id = reply_msg.sender_id
    if target_id in ENEMY_LIST:
        ENEMY_LIST.remove(target_id)
        save_enemies()
        await event.reply("**\n✅ ENEMY REMOVED\n**", parse_mode="markdown")
    else:
        await event.reply("**\nℹ️ USER IS NOT IN ENEMY LIST.\n**", parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^remove\s+all\s+enemy$"))
async def remove_all_enemy_handler(event):
    global ENEMY_LIST
    if not await admin_only(event):
        return
    ENEMY_LIST.clear()
    save_enemies()
    await event.reply("**\n✅ ALL ENEMIES REMOVED\n**", parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^help$"))
async def help_handler(event):
    if not await admin_only(event):
        return
    await event.reply(
        "```\n"
        "‌ ‌ ‌ ‌ ‌‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌  ‌T O R N A D O\n\n"
        "> status   -   a\n"
        "> join { Link }   -   Join of all account\n"
        "> leave all   -   Leave of all account\n"
        "> set reply @username   -   Set up a reply to the user\n"
        "> remove reply   -   Delete a reply from a user\n"
        "> set time NUMBER   -   Adjust message sending speed\n"
        "> set admin ID   -   Adding an admin\n"
        "> remove admin ID   -   Removed an admin\n"
        "> remove all admin   -   Remove all admins except the manager\n"
        "> setenemy   -   Add enemy & attack (Reply)\n"
        "> remove enemy   -   Remove enemy (Reply)\n"
        "> remove all enemy   -   Remove all enemies\n"
        "> list fosh   -   Show total fosh\n"
        "> add fosh TEXT   -   Add text to fosh list\n"
        "> remove fosh TEXT   -   Remove text from fosh list\n"
        "> spam TEXT   -   Custom text spam\n"
        "> spam fosh   -   Random swear spam\n"
        "> Off   -   Stop spam\n"
        "> ON   -   Reply to all accounts and write { ONLINE ✅ }\n"
        "> Ping   -   Ping replication for all accounts\n"
        "```"
    )

@manager.on(events.NewMessage(pattern=r"^status$"))
async def status_handler(event):
    if not await admin_only(event):
        return
    result = []
    for i, client in enumerate(accounts, 1):
        try:
            if await client.is_user_authorized():
                me = await client.get_me()
                result.append(f"**\n🟢 Account {i} | {me.id}\n**")
            else:
                result.append(f"**\n🔴 Account {i} | NOT LOGGED IN\n**")
        except Exception:
            result.append(f"**\n⚠️ Account {i} | ERROR\n**")
    admins_info = ""
    if EXTRA_ADMINS:
        admins_info = "\n\n👤 Admins:\n" + "\n".join(f"• {x}" for x in EXTRA_ADMINS)
    enemy_info = ""
    if ENEMY_LIST:
        enemy_info = "\n\n🎯 Enemies:\n" + "\n".join(f"• {x}" for x in ENEMY_LIST)
    await event.reply("\n".join(result) + admins_info + enemy_info, parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^set\s+reply\s+(.+)$"))
async def set_reply_handler(event):
    global REPLY_TARGETS
    if not await admin_only(event):
        return
    raw = event.pattern_match.group(1).strip()
    usernames = [u.lstrip("@") for u in raw.split() if u.strip()]
    if not usernames:
        await event.reply("```\n❌ No usernames given.\n```")
        return
    added, failed = [], []
    for uname in usernames:
        try:
            entity = await manager.get_entity(uname)
            if not any(t["id"] == entity.id for t in REPLY_TARGETS):
                REPLY_TARGETS.append({"id": entity.id, "username": uname})
                added.append(uname)
            else:
                failed.append(f"{uname} (already)")
        except Exception:
            failed.append(uname)
    lines = ["```\n"]
    if added:
        lines.append("Added:")
        for u in added:
            lines.append(f"  • @{u}")
    if failed:
        lines.append("\n❌ Failed:")
        for u in failed:
            lines.append(f"  • @{u}")
    lines.append(f"\n🎯 Total: {len(REPLY_TARGETS)}")
    lines.append("```")
    await event.reply("\n".join(lines))

@manager.on(events.NewMessage(pattern=r"^remove\s+reply$"))
async def remove_reply_handler(event):
    global REPLY_TARGETS
    if not await admin_only(event):
        return
    if not REPLY_TARGETS:
        await event.reply("**\nℹ️ NO REPLY TARGET SET\n**", parse_mode="markdown")
        return
    REPLY_TARGETS = []
    await event.reply("**\n✅ ALL REPLY TARGETS REMOVED.\n**", parse_mode="markdown")

@manager.on(events.NewMessage(pattern=r"^set\s+time\s+([\d.]+)$"))
async def set_time_handler(event):
    global SPAM_DELAY
    if not await admin_only(event):
        return
    try:
        value = float(event.pattern_match.group(1))
    except Exception:
        await event.reply("```\n❌ Invalid number.\n```")
        return
    if value < 0.1 or value > 60:
        await event.reply("```\n❌ Value must be between 0.1 and 60 seconds.\n```")
        return
    SPAM_DELAY = value
    save_settings()
    await event.reply(
        "```\n"
        f"✅ SPAM DELAY SET TO {SPAM_DELAY}s\n"
        f"💾 SAVED PERMANENTLY.\n"
        "```"
    )

@manager.on(events.NewMessage(pattern=r"^set\s+admin\s+(\d+)$"))
async def set_admin_handler(event):
    global EXTRA_ADMINS
    if not await admin_only(event):
        return
    try:
        new_id = int(event.pattern_match.group(1))
    except Exception:
        await event.reply("**\n❌ INVALID ID.\n**", parse_mode="markdown")
        return
    if new_id == MANAGER_ID:
        await event.reply("**\nℹ️ This is already the manager.\n**", parse_mode="markdown")
        return
    if new_id in EXTRA_ADMINS:
        await event.reply("**\nℹ️ Already an admin.\n**", parse_mode="markdown")
        return
    EXTRA_ADMINS.append(new_id)
    save_admins()
    await event.reply(
        "**\n"
        f"✅ ADMIN ADDED: {new_id}\n"
        f"💾 SAVED PERMANENTLY.\n"
        "**",
        parse_mode="markdown"
    )

@manager.on(events.NewMessage(pattern=r"^remove\s+admin\s+(\d+)$"))
async def remove_admin_handler(event):
    global EXTRA_ADMINS
    if not await admin_only(event):
        return
    try:
        target_id = int(event.pattern_match.group(1))
    except Exception:
        await event.reply("**\n❌ INVALID ID.\n**", parse_mode="markdown")
        return
    if target_id not in EXTRA_ADMINS:
        await event.reply("**\nℹ️ This ID is not an admin.\n**", parse_mode="markdown")
        return
    EXTRA_ADMINS.remove(target_id)
    save_admins()
    await event.reply(
        "**\n"
        f"✅ ADMIN REMOVED: {target_id}\n"
        f"💾 SAVED PERMANENTLY.\n"
        "**",
        parse_mode="markdown"
    )

@manager.on(events.NewMessage(pattern=r"^remove\s+all\s+admin$"))
async def remove_all_admin_handler(event):
    global EXTRA_ADMINS
    if not await admin_only(event):
        return
    if not EXTRA_ADMINS:
        await event.reply("**\nℹ️ No extra admins to remove.\n**", parse_mode="markdown")
        return
    count = len(EXTRA_ADMINS)
    EXTRA_ADMINS = []
    save_admins()
    await event.reply(
        "**\n"
        f"✅ REMOVED {count} ADMIN(s).\n"
        f"ℹ️ MANAGER IS STILL ADMIN.\n"
        "**",
        parse_mode="markdown"
    )

# ---------- ON / PING ----------

@manager.on(events.NewMessage(pattern=r"^ON$"))
async def on_handler(event):
    if not await admin_only(event):
        return
    chat_id = event.chat_id
    manager_msg_id = event.id

    async def send_online(client):
        try:
            if not await client.is_user_authorized():
                return
            await asyncio.sleep(random.uniform(0, STAGGER_MAX))
            try:
                await client.send_message(chat_id, "**ONLINE ✅**", reply_to=manager_msg_id, parse_mode="markdown")
            except Exception:
                try:
                    await client.send_message(chat_id, "**ONLINE ✅**", parse_mode="markdown")
                except Exception:
                    pass
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            pass

    await asyncio.gather(*(send_online(c) for c in accounts))

@manager.on(events.NewMessage(pattern=r"^Ping$"))
async def ping_handler(event):
    if not await admin_only(event):
        return
    chat_id = event.chat_id
    manager_msg_id = event.id

    async def send_ping(client):
        try:
            if not await client.is_user_authorized():
                return
            await asyncio.sleep(random.uniform(0, STAGGER_MAX))
            try:
                start = asyncio.get_event_loop().time()
                await client.get_me()
                ping_ms = int((asyncio.get_event_loop().time() - start) * 1000)
            except Exception:
                ping_ms = 0
            text = f"📶 PING : 0.{str(ping_ms).zfill(3)}"
            try:
                await client.send_message(chat_id, text, reply_to=manager_msg_id)
            except Exception:
                try:
                    await client.send_message(chat_id, text)
                except Exception:
                    pass
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            pass

    await asyncio.gather(*(send_ping(c) for c in accounts))

# ---------- SPAM ----------

@manager.on(events.NewMessage(pattern=r"^spam\s+(.+)$"))
async def spam_handler(event):
    global SPAM_RUNNING, SPAM_MODE
    if not await admin_only(event):
        return
    if SPAM_RUNNING:
        await event.reply("```\n⚠️ SPAM ALREADY RUNNING. PLEASE SEND Off FIRST.\n```")
        return
    arg = event.pattern_match.group(1).strip()
    if arg.lower() == "fosh":
        SPAM_MODE = "fosh"
    else:
        SPAM_MODE = "text"
    custom_text = arg
    chat_id = event.chat_id

    online = []
    for i, client in enumerate(accounts, 1):
        try:
            if await client.is_user_authorized():
                online.append((i, client))
        except Exception:
            pass

    if not online:
        await event.reply("```\n❌ No authorized accounts.\n```")
        return
    if SPAM_MODE == "fosh" and not FOSH_LIST:
        await event.reply("```\n❌ No fosh in list.\n```")
        return

    SPAM_RUNNING = True
    mode_label = "fosh" if SPAM_MODE == "fosh" else f"text ({custom_text})"
    reply_info = ""
    if REPLY_TARGETS:
        reply_info = f"\n🎯 Reply targets: {len(REPLY_TARGETS)}"

    await event.reply(
        "**\n"
        f"🔥 SPAM STARTED ({mode_label}) WITH {len(online)} ACCOUNTS.{reply_info}\n"
        f"⏱ DELAY : {SPAM_DELAY}s\n"
        f"🛑 PLEASE SEND Off TO STOP.\n"
        "**",
        parse_mode="markdown"
    )

    counter = {i: 0 for i, _ in online}
    flood_flags = {i: False for i, _ in online}  # اکانت‌هایی که FloodWait گرفتن
    total_rounds = 0
    fosh_index = 0

    # فلگ‌های کنترل
    stop_event = asyncio.Event()

    async def flood_clear(i, seconds):
        await asyncio.sleep(seconds)
        flood_flags[i] = False

    async def send_one(i, client, text):
        if flood_flags[i]:
            return
        try:
            await asyncio.sleep(random.uniform(0, STAGGER_MAX))
            final_text = text
            if tag_line:
                final_text = text + "\n\n" + tag_line
            if reply_to_id is not None:
                try:
                    await client.send_message(chat_id, final_text, reply_to=reply_to_id, parse_mode="html")
                except Exception:
                    await client.send_message(chat_id, final_text, parse_mode="html")
            else:
                await client.send_message(chat_id, final_text, parse_mode="html")
            counter[i] += 1
        except FloodWaitError as e:
            flood_flags[i] = True
            asyncio.create_task(flood_clear(i, e.seconds))
        except Exception:
            pass

    try:
        while SPAM_RUNNING:
            # گرفتن reply target در هر دور (اگه target تنظیم شده)
            reply_to_id, tags = await resolve_reply_target(chat_id)
            tag_line = ""
            if tags:
                tag_line = " ".join(f'<a href="tg://user?id={t["id"]}">𒆙</a>' for t in tags)

            tasks = []
            for i, client in online:
                if SPAM_MODE == "fosh":
                    text = FOSH_LIST[fosh_index % len(FOSH_LIST)]
                    fosh_index += 1
                else:
                    text = custom_text
                tasks.append(send_one(i, client, text))

            await asyncio.gather(*tasks)
            total_rounds += 1

            if not SPAM_RUNNING:
                break

            # انتظار با قابلیت قطع سریع
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=SPAM_DELAY)
                break
            except asyncio.TimeoutError:
                pass
    finally:
        SPAM_RUNNING = False
        stop_event.set()
        total_msgs = sum(counter.values())
        summary = "```\n" + "\n".join(f" ACCOUNT {i}: {c} MESSAGES" for i, c in counter.items()) + "\n```"
        try:
            await manager.send_message(
                chat_id,
                "**\n"
                f"🛑 SPAM STOPPED.\n"
                f"📊 TOTAL {total_msgs} (ROUNDS: {total_rounds})\n\n{summary}\n"
                "**",
                parse_mode="markdown"
            )
        except Exception:
            pass

@manager.on(events.NewMessage(pattern=r"^Off$"))
async def stop_handler(event):
    global SPAM_RUNNING
    if not await admin_only(event):
        return
    if not SPAM_RUNNING:
        await event.reply("**\nℹ️ NO SPAM RUNNING.\n**", parse_mode="markdown")
        return
    SPAM_RUNNING = False
    await event.reply("**\n🛑 ATTACKED STOPPED\n**", parse_mode="markdown")

# ---------- JOIN / LEAVE ----------

@manager.on(events.NewMessage(pattern=r"^join\s+(.+)$"))
async def join_handler(event):
    if not await admin_only(event):
        return
    link = event.pattern_match.group(1).strip()
    msg = await event.reply("```\n█░░░░░░░░░ 10%\n```")
    for percent in range(20, 101, 10):
        await asyncio.sleep(0.2)
        filled = percent // 10
        bar = "█" * filled + "░" * (10 - filled)
        await msg.edit(f"```\n{bar} {percent}%\n```")

    results = []

    async def try_join(i, client):
        try:
            if not await client.is_user_authorized():
                results.append(f"**\n🔴 Account {i}: not logged in\n**")
                return
            result = await join_link(client, link)
            results.append(f"**\n🟢 Account {i}: {result}\n**")
        except UserAlreadyParticipantError:
            results.append(f"**\n🟡 Account {i}: already joined\n**")
        except InviteHashInvalidError:
            results.append(f"**\n🔴 Account {i}: invalid invite\n**")
        except InviteHashExpiredError:
            results.append(f"**\n🔴 Account {i}: expired invite\n**")
        except FloodWaitError as e:
            results.append(f"**\n🟠 Account {i}: flood {e.seconds}s\n**")
        except Exception as e:
            results.append(f"**\n🔴 Account {i}: {e}\n**")

    await asyncio.gather(*(try_join(i, c) for i, c in enumerate(accounts, 1)))

    await event.reply(
        "**\n✅ JOIN PROCESS FINISHED.\n\n" + "\n".join(results) + "\n**",
        parse_mode="markdown"
    )

@manager.on(events.NewMessage(pattern=r"^leave\s+all$"))
async def leave_handler(event):
    if not await admin_only(event):
        return
    msg = await event.reply("```\n⏳ Leave started...\n█░░░░░░░░░ 10%\n```")
    for percent in range(20, 101, 10):
        await asyncio.sleep(0.2)
        filled = percent // 10
        bar = "█" * filled + "░" * (10 - filled)
        await msg.edit(f"```\n⏳ Leave started...\n{bar} {percent}%\n```")

    results = []

    async def try_leave(i, client):
        try:
            if not await client.is_user_authorized():
                results.append(f"**\n🔴 Account {i}: not logged in\n**")
                return
            await client.delete_dialog(event.chat_id)
            results.append(f"**\n🟢 Account {i}: left\n**")
        except FloodWaitError as e:
            results.append(f"**\n🟠 Account {i}: flood {e.seconds}s\n**")
        except Exception as e:
            results.append(f"**\n🔴 Account {i}: {e}\n**")

    await asyncio.gather(*(try_leave(i, c) for i, c in enumerate(accounts, 1)))

    await event.reply(
        "**\n✅ LEAVE PROCESS FINISHED.\n\n" + "\n".join(results) + "\n**",
        parse_mode="markdown"
    )

# ---------- MAIN ----------

async def main():
    print("=" * 40)
    print("Telegram Manager")
    print("=" * 40)
    load_settings()
    load_admins()
    load_enemies()
    await login_manager()
    print("\nChecking accounts...\n")
    await load_accounts()
    print("\nON ✅")
    await manager.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"FATAL: {e}")