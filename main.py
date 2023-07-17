import json
import openai
import telebot
import whisper

# Load keys
with open("user_data/keys.json", "r", encoding="utf-8") as f:
    keys_dic = json.load(f)

with open("start.txt", "r", encoding="utf-8") as f:
    start_message = f.read()

with open("help.txt", "r", encoding="utf-8") as f:
    help_message = f.read()

# Setup chatGPT
openai.api_key = keys_dic["chatGPT"]
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Setup Whisper
model_types = ["tiny", "base", "small", "medium", "large"]
selected_model = "base"
whisper_model = whisper.load_model(selected_model)

# Setup Telegram bot
bot = telebot.TeleBot(keys_dic["telegram"])

def get_answer(message):
    '''
    Takes a Telebot message oject, passes its text to chatGPT
    and returns the answer.
    '''
    messages.append({"role": "user", "content": message.text})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    return(reply)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = "user_data/" + str(message.from_user.id) + "_voice.ogg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Processing audio...")
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
        selected_model = message.text[1:]
        whisper_model = whisper.load_model(selected_model) # No carga, fuera de scope.
        answer = "Modelo " + selected_model + " cargado."
    elif (message.text == "/modelo"):
        answer = "El modelo de Whisper en uso es " + selected_model
    else:
        answer = get_answer(message)

    bot.reply_to(message, answer)

bot.infinity_polling()
