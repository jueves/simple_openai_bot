# Simple OpenAI Telegram Bot
- When it gets a text message it passes it to ChatGPT and returns the answer.  
- When it gets a voice note it passes it through Whisper and returns it as text.
- You can also send a URL to an audio file and it will be transcribed.
- If you reply to a message (no matter your reply) it returns a summary of the message you replied to.


# Installation
- Use Docker image `bro3jo2/simpleopenaibot:latest`.
- Set the environment variables:
    - `CHATGPT_KEY` You get it in your [OpenAI account settings](https://platform.openai.com/account/api-keys)
    - `TELEGRAM_KEY` Create it using [BotFather](https://web.telegram.org/a/#93372553) 
    - `MODELS` Comma separated list of the Whisper models that will be avaible. This allows lo exclude larger models that require much more resources.
    - `DEFAULT_MODEL` The Whisper model in use when the app starts.
- Run docker compose using `simple_openai_bot.yml`.

# Ussage
This is a Telegram Bot, you interact with it through Telegram chat.
- `/start` Shows welcome message.
- `/ayuda` Shows list of possible commands.
- `/modelo` Shows the Whisper model in use.
- `/tiny`, `/base`, `/small`, `/medium` and `/large` change the Whisper model.
- `/clear` Starts a new conversation with ChatGPT.
- Any other text message is sent to chatGPT and its answer is returned.
- Send any voice note and a transcription is sent back.
- Reply (with whatever text) to a message and a summary is returned.
- Send a URL to an audio file and you will get a transcription. Depending on the model in use, the lenght of the audio and the hardware capabilities, it can be better to set a scheduled message for late at night, because the bot could get busy for hours long.
