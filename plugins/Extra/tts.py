


import traceback
from asyncio import get_running_loop
from io import BytesIO
from googletrans import Translator
from gtts import gTTS
from pyrogram import Client, filters
from pyrogram.types import Message


def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@Client.on_message(filters.command("tts"))
async def text_to_speech(bot, message: Message):
    hk = await bot.ask(chat_id = message.from_user.id, text = "Now send me your text.")
    if hk.text:
        m = await hk.reply_text("Processing")
        text = hk.text
        try:
            loop = get_running_loop()
            audio = await loop.run_in_executor(None, convert, text)
            await hk.reply_audio(audio)
            await m.delete()
            audio.close()
        except Exception as e:
            await m.edit(e)
            e = traceback.format_exc()
            print(e)
    else:
        await hk.reply_text("Send me only text Buddy.")
