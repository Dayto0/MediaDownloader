#!/usr/bin/env python3
import os
import re
import shutil
import logging
import tempfile
import asyncio

from yt_dlp import YoutubeDL
from telegram import InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_TOKEN_HERE"
MAX_SEND_BYTES = 50 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL_RE = re.compile(r"https?://\S+")
ALLOWED_DOMAINS = (
    "youtube.com", "youtu.be",
    "tiktok.com", "vm.tiktok.com",
    "instagram.com", "www.instagram.com", "instagram.f"
)

def url_is_supported(url: str) -> bool:
    for d in ALLOWED_DOMAINS:
        if d in url:
            return True
    return False

async def download_video(url: str, tmpdir: str) -> str:
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "postprocessors": [{
            "key": "FFmpegVideoRemuxer",
            "preferedformat": "mp4",
        }],
    }

    loop = asyncio.get_running_loop()

    def _sync_download():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                try:
                    filename = ydl.prepare_filename(info)
                except Exception:
                    filename = None
                if filename:
                    base, _ = os.path.splitext(filename)
                    candidate = base + ".mp4"
                    if os.path.exists(candidate):
                        return candidate
                    if os.path.exists(filename):
                        return filename
                files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
                files = [f for f in files if os.path.isfile(f)]
                if not files:
                    return ""
                files.sort(key=lambda p: os.path.getsize(p), reverse=True)
                return files[0]
        except Exception:
            logging.exception("yt-dlp error")
            return ""

    return await loop.run_in_executor(None, _sync_download)

async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg is None:
        return

    text = (msg.text or "") + " " + (msg.caption or "")
    urls = URL_RE.findall(text)
    if not urls:
        await msg.reply_text("🔗❓")
        return

    target_url = None
    for u in urls:
        if url_is_supported(u):
            target_url = u
            break

    if not target_url:
        await msg.reply_text("🚫")
        return

    status_message = await msg.reply_text("⏳")

    tmpdir = tempfile.mkdtemp(prefix="tgdl_")
    try:
        file_path = await download_video(target_url, tmpdir)
        if not file_path or not os.path.exists(file_path):
            try:
                await status_message.edit_text("❌")
            except Exception:
                await msg.reply_text("❌")
            return

        size = os.path.getsize(file_path)
        logging.info("Downloaded file %s (%d bytes)", file_path, size)

        if size > MAX_SEND_BYTES:
            try:
                await status_message.edit_text("⚠️")
            except Exception:
                await msg.reply_text("⚠️")
            return

        try:
            await status_message.edit_text("⏳")
        except Exception:
            pass

        with open(file_path, "rb") as f:
            await context.bot.send_video(chat_id=msg.chat_id, video=InputFile(f), supports_streaming=True)
        try:
            await status_message.delete()
        except Exception:
            pass
    except Exception:
        logging.exception("handler error")
        try:
            await status_message.edit_text("❌")
        except Exception:
            await msg.reply_text("❌")
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Caption(), handle_message))
    print("Started")
    app.run_polling()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import os
import re
import shutil
import logging
import tempfile
import asyncio

from yt_dlp import YoutubeDL
from telegram import InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_TOKEN_HERE"
MAX_SEND_BYTES = 50 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL_RE = re.compile(r"https?://\S+")
ALLOWED_DOMAINS = (
    "youtube.com", "youtu.be",
    "tiktok.com", "vm.tiktok.com",
    "instagram.com", "www.instagram.com", "instagram.f"
)

def url_is_supported(url: str) -> bool:
    for d in ALLOWED_DOMAINS:
        if d in url:
            return True
    return False

async def download_video(url: str, tmpdir: str) -> str:
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "postprocessors": [{
            "key": "FFmpegVideoRemuxer",
            "preferedformat": "mp4",
        }],
    }

    loop = asyncio.get_running_loop()

    def _sync_download():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                try:
                    filename = ydl.prepare_filename(info)
                except Exception:
                    filename = None
                if filename:
                    base, _ = os.path.splitext(filename)
                    candidate = base + ".mp4"
                    if os.path.exists(candidate):
                        return candidate
                    if os.path.exists(filename):
                        return filename
                files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
                files = [f for f in files if os.path.isfile(f)]
                if not files:
                    return ""
                files.sort(key=lambda p: os.path.getsize(p), reverse=True)
                return files[0]
        except Exception:
            logging.exception("yt-dlp error")
            return ""

    return await loop.run_in_executor(None, _sync_download)

async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg is None:
        return

    text = (msg.text or "") + " " + (msg.caption or "")
    urls = URL_RE.findall(text)
    if not urls:
        await msg.reply_text("🔗❓")
        return

    target_url = None
    for u in urls:
        if url_is_supported(u):
            target_url = u
            break

    if not target_url:
        await msg.reply_text("🚫")
        return

    status_message = await msg.reply_text("⏳")

    tmpdir = tempfile.mkdtemp(prefix="tgdl_")
    try:
        file_path = await download_video(target_url, tmpdir)
        if not file_path or not os.path.exists(file_path):
            try:
                await status_message.edit_text("❌")
            except Exception:
                await msg.reply_text("❌")
            return

        size = os.path.getsize(file_path)
        logging.info("Downloaded file %s (%d bytes)", file_path, size)

        if size > MAX_SEND_BYTES:
            try:
                await status_message.edit_text("⚠️")
            except Exception:
                await msg.reply_text("⚠️")
            return

        try:
            await status_message.edit_text("⏳")
        except Exception:
            pass

        with open(file_path, "rb") as f:
            await context.bot.send_video(chat_id=msg.chat_id, video=InputFile(f), supports_streaming=True)
        try:
            await status_message.delete()
        except Exception:
            pass
    except Exception:
        logging.exception("handler error")
        try:
            await status_message.edit_text("❌")
        except Exception:
            await msg.reply_text("❌")
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Caption(), handle_message))
    print("Started")
    app.run_polling()

if __name__ == "__main__":
    main()
