
import os
import whisper
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# فقط مخصوص کاربر: Mehdi (id: 876485855)
ALLOWED_USER_ID = 876485855
model = whisper.load_model("base")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text("سلام! فایل صوتی بفرست تا برات به متن تبدیل کنم.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    audio_file = await update.message.voice.get_file() if update.message.voice else await update.message.audio.get_file()
    file_path = f"temp_{update.message.message_id}.ogg"
    await audio_file.download_to_drive(file_path)
    result = model.transcribe(file_path)
    os.remove(file_path)
    await update.message.reply_text(result["text"])

app = ApplicationBuilder().token("7672016924:AAH_G8Jtncuq9q30v9Wvtuc_H5MrYlXwa3s").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))

if __name__ == '__main__':
    app.run_polling()
