# Simple OpenAI Telegram Bot
- When it gets a text message it passes it to ChatGPT and returns the answer.  
- When it gets a voice note it passes it through Whisper and returns it as text.
- You can also send a URL to an audio file and it will be transcribed.
- If you reply to a message (no matter your reply) it returns a summary of the message you replied to.


# Installation
- Use Docker image `bro3jo2/simpleopenaibot:latest`.
- Set your keys with the environment variables `CHATGPT_KEY` and `TELEGRAM_KEY`.
- You can also set which models will be available setting them as a comma separated list in the environment variable `MODELS`. This allows lo exclude larger models that require much more resources.

# Ussage
This is a Telegram Bot, you interact with it through Telegram chat.
- `/start` Shows welcome message.
- `/ayuda` Shows list of possible commands.
- `/modelo` Shows the Whisper model in use.
- `/tiny`, `/base`, `/small`, `/medium` and `/large` change the Whisper model.
- Any other text message is sent to chatGPT and its answer is returned.
- Send any voice note and a transcription is sent back.
- Reply (with whatever text) to a message and a summary is returned.
- Send a URL to an audio file and you will get a transciption. If the audio is long, it can be better to set a scheduled message for late at night, because the bot could get busy for hours long.
