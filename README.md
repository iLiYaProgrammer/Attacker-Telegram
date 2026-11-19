🤖 Telegram Spammer & Manager Bot

<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python" />
<img src="https://img.shields.io/badge/Telethon-Latest-blue?style=for-the-badge&logo=telegram" alt="Telethon" />
<img src="https://img.shields.io/badge/License-Educational-red?style=for-the-badge" alt="License" />

ربات مدیریت و اسپم تلگرام به صورت چند اکانتی (Multi-Account) و ناهمگام (Async)

</div>

---

⚠️ سلب مسئولیت

این پروژه فقط برای اهداف آموزشی و تست قدرت API تلگرام طراحی شده است. استفاده از این اسکریپت برای آزار و اذیت، ارسال پیام‌های مزاحم، یا نقض قوانین تلگرام کاملاً ممنوع است. مسئولیت هرگونه سوءاستفاده یا مسدود شدن اکانت شما بر عهده خود شماست.

---

✨ امکانات

· 🚀 مدیریت ۱۰ اکانت به صورت همزمان
· ⚡ ناهمگام (Async) با استفاده از کتابخانه asyncio برای سرعت بالا
· 🛡 قابلیت مدیریت ادمین‌ها و افزودن ادمین‌های جدید
· 🎯 سیستم دشمن (Enemy System) برای پاسخ خودکار به کاربران مشخص
· 💬 اسپم سفارشی یا اسپم با لیست فحش‌های ذخیره شده
· 🔗 ورود و خروج گروهی (Join / Leave) برای تمامی اکانت‌ها
· 💾 ذخیره خودکار تنظیمات در فایل‌های txt تا بعد از ری‌استارت پاک نشوند
· ⏱ تنظیم سرعت و زمان تاخیر (Delay) بین پیام‌ها

---

🛠 پیش‌نیازها

· Python 3.8 یا بالاتر

برای نصب کتابخانه مورد نیاز، از دستور زیر استفاده کنید:

```bash
pip install -r requirements.txt
```

(یا به صورت دستی: pip install telethon)

---

🚀 نصب و راه‌اندازی

۱. پروژه را کلون کنید:

```bash
git clone https://github.com/your-username/Telegram-Manager.git
cd Telegram-Manager
```

۲. کتابخانه‌ها را نصب کنید:

```bash
pip install -r requirements.txt
```

۳. فایل main.py را اجرا کنید:

```bash
python main.py
```

۴. در فایل main.py مقادیر API_ID و API_HASH خود را (از my.telegram.org) جایگزین کنید.
۵. اکانت‌ها را با شماره تلفن در اولین اجرا لاگین کنید.

نکته: فایل‌های جانبی (settings.txt، admins.txt، enemies.txt، fosh.txt) به صورت خودکار در اولین اجرا ساخته می‌شوند.

---

📜 دستورات ربات (در چت با منیجر)

🛠 مدیریت:

· help : نمایش لیست دستورات
· status : بررسی وضعیت اکانت‌ها
· set admin [ID] : افزودن ادمین
· remove admin [ID] : حذف ادمین
· remove all admin : حذف تمامی ادمین‌ها

🔥 اسپم و حمله:

· spam [متن] : شروع اسپم سفارشی
· spam fosh : شروع اسپم با لیست فحش‌ها
· Off : توقف اسپم
· set time [ثانیه] : تنظیم تاخیر بین پیام‌ها (بین 0.1 تا 60)

🎯 مدیریت دشمن و ریپلای:

· set reply @username : تنظیم کاربر برای ریپلای کردن
· remove reply : حذف تارگت‌های ریپلای
· setenemy : اضافه کردن کاربر به لیست دشمن (باید روی پیامش ریپلای کنی)
· remove enemy : حذف کاربر از لیست دشمن (با ریپلای)

📚 مدیریت لیست فحش:

· list fosh : نمایش تعداد کل فحش‌ها
· add fosh [متن] : اضافه کردن متن جدید
· remove fosh [متن] : حذف متن از لیست

🔗 گروه‌ها:

· join [لینک] : ورود همه اکانت‌ها به گروه/کانال
· leave all : خروج همه اکانت‌ها از چت فعلی
· Ping : تست پینگ اکانت‌ها
· ON : ارسال پیام آنلاین بودن از سمت همه اکانت‌ها

---

🏗️ ساختار پروژه

```text
Telegram-Manager/
├── main.py           # فایل اصلی برنامه
├── requirements.txt  # لیست کتابخانه‌های مورد نیاز
├── session/          # پوشه ذخیره لاگین اکانت‌ها (خودکار ساخته می‌شود)
├── settings.txt      # تنظیمات تاخیر
├── admins.txt        # لیست ادمین‌ها
├── enemies.txt       # لیست دشمنان
└── fosh.txt          # لیست متن‌های اسپم
```

---

<div align="center">

⭐ ستاره یادت نره ⭐

</div>
