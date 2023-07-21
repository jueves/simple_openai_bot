# Simple OpenAi Telegram Bot
- When it gets a text message it passes it to ChatGPT and returns the answer.  
- When it gets an audio it passes it through Whisper and returns it as text.

Telegram comands:
- `/start` Shows welcome message.
- `/ayuda` Shows list of possible commands.
- `/modelo` Shows the Whisper model in use.
- `/tiny`, `/base`, `/small` and `/medium` change the Whisper model. _Large_ model is removed due to limitations in the hardware the program runs.

# To do
- [X] Add option to easily set from the server side the models that will be available to users.
- [ ] Manage concurrence regarding diferent model types being used.
