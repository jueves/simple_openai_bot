import json
import openai
import telebot
import whisper
import os

print("Versión con variables de entorno.")
model_types = os.environ.get("MODELS", "tiny,base,small").split(",")
print(model_types)

# Load keys
with open("user_data/keys.json", "r", encoding="utf-8") as f:
    keys_dic = json.load(f)

with open("start.txt", "r", encoding="utf-8") as f:
    start_message = f.read()

with open("help.txt", "r", encoding="utf-8") as f:
    help_message = f.read()

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

# Setup chatGPT
openai.api_key = keys_dic["chatGPT"]
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Setup Whisper
class WhisperModel:
    def __init__(self, model_type):
        self.set_type(model_type)

    def set_type(self, model_type):
        self.model_type = model_type
        self.model = whisper.load_model(model_type)
    
    def get_type(self):
        return(self.model_type)
    
    def transcribe(self, file_name):
        text = self.model.transcribe(file_name)
        return(text)

whisper_model = WhisperModel("base")

# Setup Telegram bot
bot = telebot.TeleBot(keys_dic["telegram"])

def get_answer(message, summary=False):
    '''
    Takes a Telebot message oject, passes its text to chatGPT
    and returns the answer.
    '''
    text = message.text
    header = ""
    if (summary):
        text =  prompt + "\n" + text
        header = "Resumen:\n"
    messages.append({"role": "user", "content": text})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
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
    result = whisper_model.transcribe(file_name)
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
        whisper_model.set_type(message.text[1:])
        answer = "Modelo " + whisper_model.get_type() + " cargado."
    elif (message.text in ["/modelo", "/model"]):
        answer = "El modelo de Whisper en uso es " + whisper_model.get_type()
    elif (message.reply_to_message is not None):
        answer = get_answer(message.reply_to_message, summary=True)
    else:
        answer = get_answer(message)

    bot.reply_to(message, answer, parse_mode='Markdown')

bot.infinity_polling()
