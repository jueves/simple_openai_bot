# Simple OpenAI Telegram Bot
- When it gets a text message it passes it to ChatGPT and returns the answer.  
- When it gets an audio it passes it through Whisper and returns it as text.
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
- Any other text message is sent to chatGPT and its answer is returned to you.
- Send any voice note and a transcription is sent back to yo.
- Reply (with whatever text) to a message and a summary of the message is replied to you.

