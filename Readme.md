# Simple OpenAI Telegram Bot
- When it gets a text message it passes it to ChatGPT and returns the answer.  
- When it gets an audio it passes it through Whisper and returns it as text.

Telegram comands:
- `/start` Shows welcome message.
- `/ayuda` Shows list of possible commands.
- `/modelo` Shows the Whisper model in use.
- `/tiny`, `/base`, `/small`, `/medium` and `/large` change the Whisper model. The list of available models can be set in the docker compose file. This allows lo exclude larger models that require much more resources.

# Ussage
Add your keys to `simple_openai_bot.yml` as environment variables and run container in Docker.  


# To do
- [X] Add option to easily set from the server side the models that will be available to users.
- [ ] Manage concurrence regarding diferent model types being used.
- [ ] Take audio messages and not just voice messages.
