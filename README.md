
## **MediaDownloader** — Telegram bot that downloads and sends videos from YouTube Shorts / TikTok / Instagram Reels.

---

## Description

Lightweight Python Telegram bot. When a user sends a supported short/reel link, the bot downloads the video with `yt-dlp` and returns the MP4 to the chat.
---

## Requirements (packages)

### System

* `ffmpeg` — required by `yt-dlp` for merging/remuxing. Install via system package manager or download and add to PATH.

### Python packages

Install into a virtual environment:

```bash
python -m pip install --upgrade pip
pip install python-telegram-bot yt-dlp pytz tzlocal==4.2.1
```

Suggested `requirements.txt`:

```
python-telegram-bot
yt-dlp
pytz
tzlocal==4.2.1
```

---

## How to use

1. Clone or copy the repo and open the main script (`telegram_dl_bot.py`).
2. Put your bot token in the script:

```py
BOT_TOKEN = "123456:ABC-DEF..."
```

3. Ensure `ffmpeg` is installed and available in PATH.
4. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

5. Install Python dependencies (see Requirements).
6. Run the bot:

```bash
python telegram_dl_bot.py
```

7. Send a YouTube Shorts / TikTok / Instagram Reels link to the bot — it will reply with emoji status and send the video if downloadable and within size limits.

---

## **MediaDownloader** — Telegram-бот для скачивания и отправки видео из YouTube Shorts / TikTok / Instagram Reels

---

## Описание

Небольшой бот на Python. При получении ссылки на короткое видео бот скачивает ролик с помощью `yt-dlp` и отправляет MP4 в чат.

---

## Требования (пакеты)

### Системные

* `ffmpeg` — нужен для склейки/перекодирования. Установить через пакетный менеджер или скачай сборку и добавь в PATH.

### Python-пакеты

```bash
python -m pip install --upgrade pip
pip install python-telegram-bot yt-dlp pytz tzlocal==4.2.1
```

`requirements.txt`:

```
python-telegram-bot
yt-dlp
pytz
tzlocal==4.2.1
```

---

## Как использовать

1. Склонируй репозиторий или помести файл `telegram_dl_bot.py` в папку.
2. Вставь токен бота в файл:

```py
BOT_TOKEN = "123456:ABC-DEF..."
```

3. Установи `ffmpeg` и проверь, что он доступен в PATH.
4. Рекомендуется создать виртуальное окружение:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

5. Установи зависимости (см. выше).
6. Запусти бота:

```bash
python telegram_dl_bot.py
```

7. Отправь боту ссылку на Shorts / Reel / TikTok — бот покажет эмоджи-статус и пришлёт видео, если удалось скачать и размер в пределах лимита.
