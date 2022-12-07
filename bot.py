import telebot
import os, sys
import speech_recognition as sr
from pydub import AudioSegment
import uuid

bot = telebot.TeleBot("???")

language = 'ru_RU'
r = sr.Recognizer()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            return text
        except:
            return None

@bot.message_handler(content_types='text')
def new_message(msg):
    bot.reply_to(msg, (
        "🔥 Привет! Я бот, который поможет тебе преобразовать голосовые сообщения в текст! "
        "Просто перешли голосовое сообщение или отправь свое, а я преобразую его в текст и отправлю тебе:3\n\n"
        "Мой создатель - WiSpace, телеграмм канал - https://t.me/wispace_ru,"
        " сайт - https://wispace.ru, умный ИИ чат бот Аня<3 - https://t.me/aispace_bot"
    ))


@bot.message_handler(content_types=['voice'])
def new_voice_message(msg):
    q = True
    try:
        file_info = bot.get_file(msg.voice.file_id)

        if file_info.file_size > 3000000:
            bot.reply_to(
                msg,
                "Извини, данное голосовое сообщение слишком большое для обработки(")
            q = False
            return
        downloaded_file = bot.download_file(file_info.file_path)
        path = "voice/" + str(uuid.uuid4())

        with open(path + '.ogg', 'wb') as f:
            f.write(downloaded_file)

        ogg_to_wav = AudioSegment.from_ogg(path + '.ogg')
        ogg_to_wav.export(path + ".wav", format="wav")

        text = recognise(path + '.wav')
    except:
        bot.reply_to(msg, "Ошибка при обработке голосового сообщения.")
        print(sys.exc_info())
        return
    finally:
        if q:
            os.remove(path + '.ogg')
            os.remove(path + '.wav')

    bot.reply_to(msg, text)

bot.infinity_polling()
