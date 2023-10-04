import os
import openai
import telebot
import whisper

# Load variables in .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Error loading dotenv, .env file won't be used.")

# Load variables
MODEL_TYPES = os.environ.get("MODELS", "tiny,base").split(",")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", MODEL_TYPES[0])
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
audio2text = {"model": whisper.load_model(DEFAULT_MODEL), "type": DEFAULT_MODEL, "available":True}

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


def link_processing(message):
    '''
    Gets a message whose content is a URL
    Downloads URL file
    Replies to sender with audio file transciption.
    '''
    try:
        answer = transcribe_audio(message, message.text)
    except:
        answer = "Ocurrió un error. ¿Seguro que el link es correcto?"

    if (len(answer) < 300):
        bot.reply_to(message, answer)
    else:
        txt_file_name = str(message.from_user.id) + "_transcript.txt"
        with open(txt_file_name, "w") as text_file:
            text_file.write(answer)
        with open(txt_file_name, "r") as text_file:
            bot.send_document(message.chat.id, reply_to_message_id=message.message_id, document=text_file)


       

def transcribe_audio(message, file_name):
    '''
    Gets a message whose content ask for an audio transcription and the file
    name of that audio.
    Returns audio transcription.
    '''
    if audio2text["available"]:
        audio2text["available"] = False
        bot.reply_to(message, "Procesando audio...")
        result = audio2text["model"].transcribe(file_name, language="es")
        answer = result["text"]
        audio2text["available"] = True
    else:
        answer = BUSY_MESSAGE
    return(answer)
    

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    '''
    Gets a message with voice.
    Replies to sender with voice transcription.
    '''
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = str(message.from_user.id) + "_voice.ogg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    answer = transcribe_audio(message, file_name)
    bot.reply_to(message, answer)

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
        if (message.text[1:] == audio2text["type"]):
            answer = "El modelo {model} ya está activo.".format(model=message.text[1:])
        elif audio2text["available"]:
            audio2text["available"] = False
            bot.reply_to(message, "Cargando modelo...")
            audio2text["model"] = whisper.load_model(message.text[1:])
            audio2text["type"] = message.text[1:]
            audio2text["available"] = True
            answer = "Modelo " + audio2text["type"] + " cargado."
        else:
            bot.reply_to(message, BUSY_MESSAGE)
    elif (message.text in ["/modelo", "/model"]):
        answer = "El modelo de Whisper en uso es " + audio2text["type"]
    elif (message.text[:4] == "http"):
        link_processing(message)
        answer = ""
    elif (message.text in ["/clear", "/limpiar"]):
        try:
            del messages_dic[message.from_user.id]
        except KeyError:
            pass
        answer = "Historial de chatGPT borrado."
    elif (message.reply_to_message is not None):
        answer = get_answer(message.reply_to_message, summary=True)
    else:
        answer = get_answer(message)

    bot.reply_to(message, answer, parse_mode='Markdown')

bot.infinity_polling()
