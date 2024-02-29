import os
import telebot
from audio_utils  import Whisper4Bot
from text_utils import TextWizard

TELEGRAM_KEY = os.environ.get("TELEGRAM_KEY")
MODEL_TYPES = os.environ.get("MODELS", "tiny,base").split(",")

with open("text/start.txt", "r", encoding="utf-8") as f:
    start_message = f.read()

with open("text/help.txt", "r", encoding="utf-8") as f:
    help_message = f.read()
    for model in MODEL_TYPES:
        help_message += "/" + model + "\n"

# Setup Telegram bot
bot = telebot.TeleBot(TELEGRAM_KEY)

# Setup audio and text managers
audio2text = Whisper4Bot(bot)
textwizard = TextWizard(bot)

@bot.message_handler(content_types=['voice', 'document', 'audio'])
def audio_processing(message):
    '''
    Gets a message with audio.
    Replies to sender with audio transcription.
    '''
    audio2text.transcribe(message)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    '''
    Takes all incoming messages and returns answers.
    '''
    if (message.text == "/start"):
        answer = start_message + help_message
    elif (message.text in ["/Ayuda", "/ayuda", "/help"]):
        answer = help_message
    elif (message.text[1:] in MODEL_TYPES):
        answer = audio2text.load_model(message, message.text[1:])
    elif (message.text in ["/modelo", "/model"]):
        answer = "El modelo de Whisper en uso es " + audio2text.type
    elif (message.text[:4] == "http"):
        answer = audio2text.transcribe(message)
    elif (message.text in ["/clear", "/limpiar"]):
        answer = textwizard.clear(message)
    elif (message.reply_to_message is not None):
        answer = textwizard.get_summary(message.reply_to_message)
    else:
        answer = textwizard.get_answer(message)

    bot.reply_to(message, answer, parse_mode='Markdown')

bot.infinity_polling()
