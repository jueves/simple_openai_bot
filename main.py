import json
import openai
import telebot
import whisper

# Load keys
with open("user_data/keys.json", "r", encoding="utf-8") as f:
    keys_dic = json.load(f)

# Setup chatGPT
openai.api_key = keys_dic["chatGPT"]
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Setup Whisper
whisper_model = whisper.load_model("base")

# Setup Telegram bot
bot = telebot.TeleBot(keys_dic["telegram"])

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
    Takes a Telebot message oject, passes its text to chatGPT
    and returns the answer.
    '''
    messages.append({"role": "user", "content": message.text})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    
    reply = chat.choices[0].message.content

    bot.reply_to(message, reply)

bot.infinity_polling()
