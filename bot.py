import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك ❤️\nأرسل الفيديو وسأجهزه لريلز إنستغرام بدقة 1080p."
    )

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ جاري تجهيز الفيديو...")

    file = await update.message.video.get_file()
    await file.download_to_drive("input.mp4")

    result = subprocess.run([
        "ffmpeg", "-y", "-i", "input.mp4",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-preset", "fast",
        "-crf", "20", "-c:a", "aac",
        "output.mp4"
    ], capture_output=True)

    if result.returncode == 0:
        await update.message.reply_video(
            video=open("output.mp4", "rb"),
            caption="❤️ الفيديو جاهز لريلز إنستغرام بدقة 1080p"
        )
    else:
        await msg.edit_text("حدث خطأ أثناء تعديل الفيديو.")

    for name in ["input.mp4", "output.mp4"]:
        if os.path.exists(name):
            os.remove(name)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, video))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
