import os
import openai
import telebot
import whisper

# Load variables
model_types = os.environ.get("MODELS", "tiny,base").split(",")
telegram_key = os.environ.get("TELEGRAM_KEY")
chatGPT_key = os.environ.get("CHATGPT_KEY")

with open("start.txt", "r", encoding="utf-8") as f:
    start_message = f.read()

with open("help.txt", "r", encoding="utf-8") as f:
    help_message = f.read()
for model in model_types:
    help_message += "/" + model + "\n"

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

# Setup chatGPT
openai.api_key = chatGPT_key
messages_dic = { "default": [ {"role": "system", "content": "You are a intelligent assistant."} ] }
#messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Setup Whisper
audio2text = {"model": whisper.load_model("base"), "type": "base"}

# Setup Telegram bot
bot = telebot.TeleBot(telegram_key)

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
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = "user_data/" + str(message.from_user.id) + "_voice.ogg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Procesando audio...")
    result = audio2text["model"].transcribe(file_name)
    bot.reply_to(message, result["text"])


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    '''
    Takes all incoming messages and returns answers.
    '''
    if (message.text == "/start"):
        answer = start_message + help_message
    elif (message.text in ["/Ayuda", "/ayuda", "/help"]):
        answer = help_message
    elif (message.text[1:] in model_types):
        bot.reply_to(message, "Cargando modelo...")
        audio2text["type"] = message.text[1:]
        audio2text["model"] = whisper.load_model(message.text[1:])
        answer = "Modelo " + audio2text["type"] + " cargado."
    elif (message.text in ["/modelo", "/model"]):
        answer = "El modelo de Whisper en uso es " + audio2text["type"]
    elif (message.reply_to_message is not None):
        answer = get_answer(message.reply_to_message, summary=True)
    else:
        answer = get_answer(message)

    bot.reply_to(message, answer, parse_mode='Markdown')

bot.infinity_polling()
