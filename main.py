import os
import openai
import telebot
import whisper

# Load variables
MODEL_TYPES = os.environ.get("MODELS", "tiny,base").split(",")
TELEGRAM_KEY = os.environ.get("TELEGRAM_KEY")
CHATGPT_KEY = os.environ.get("CHATGPT_KEY")
BUSY_MESSAGE = "El modelo Whisper está ocupado, inténtelo de nuevo en unos minutos."

with open("start.txt", "r", encoding="utf-8") as f:
    start_message = f.read()

with open("help.txt", "r", encoding="utf-8") as f:
    help_message = f.read()
for model in MODEL_TYPES:
    help_message += "/" + model + "\n"

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

# Setup chatGPT
openai.api_key = CHATGPT_KEY
messages_dic = {}

# Setup Whisper
audio2text = {"model": whisper.load_model("base"), "type": "base", "available":True}

# Setup Telegram bot
bot = telebot.TeleBot(TELEGRAM_KEY)

def get_answer(message, summary=False):
    '''
    Takes a Telebot message oject, passes its text to chatGPT
    and returns the answer.
    '''
    if (message.from_user.id not in messages_dic):
        messages_dic[message.from_user.id] =  [{'role': 'system', 'content': 'You are a intelligent assistant.'}]
    
    text = message.text
    header = ""
    if (summary):
        text =  prompt + "\n" + text
        header = "Resumen:\n"

    messages_dic[message.from_user.id].append({"role": "user", "content": text})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_dic[message.from_user.id])
    reply = chat.choices[0].message.content
    return(header + reply)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    if audio2text["available"]:
        audio2text["available"] = False
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = str(message.from_user.id) + "_voice.ogg"
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Procesando audio...")
        result = audio2text["model"].transcribe(file_name)
        bot.reply_to(message, result["text"])
        audio2text["available"] = True
    else:
        bot.reply_to(message, BUSY_MESSAGE)


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
        if audio2text["available"]:
            audio2text["available"] = False
            bot.reply_to(message, "Cargando modelo...")
            audio2text["type"] = message.text[1:]
            audio2text["model"] = whisper.load_model(message.text[1:])
            answer = "Modelo " + audio2text["type"] + " cargado."
            audio2text["available"] = True
        else:
            bot.reply_to(message, BUSY_MESSAGE)
    elif (message.text in ["/modelo", "/model"]):
        answer = "El modelo de Whisper en uso es " + audio2text["type"]
    elif (message.reply_to_message is not None):
        answer = get_answer(message.reply_to_message, summary=True)
    else:
        answer = get_answer(message)

    bot.reply_to(message, answer, parse_mode='Markdown')

bot.infinity_polling()
