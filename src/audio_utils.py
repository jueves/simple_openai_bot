import whisper
import os

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
LONGEST_MESSAGE = 4096

class Whisper4Bot:
    def __init__(self, bot, default_model=DEFAULT_MODEL, longest_message=LONGEST_MESSAGE):
        self.bot = bot
        self.type = default_model
        self.model = whisper.load_model(default_model)       
        self.available = True
        self.longest_message = longest_message

    def load_model(self, message, model_type):
        if model_type == self.type:
            answer = "El modelo {model} ya está activo.".format(model=model_type)
        elif self.available:
            self.available = False
            self.bot.reply_to(message, "Cargando modelo...")
            try:
                self.model = whisper.load_model(model_type)
                self.type = model_type
                answer = "Modelo {model} cargado.".format(model=model_type)
            except Exception as e:
                answer = "ERROR: El modelo no pudo ser cargado.\n{error}".format(error=e)
            self.available = True
        else:
            answer = "El modelo Whisper está ocupado, inténtelo de nuevo en unos minutos."
        return(answer)
    
    def transcribe(self, message):
        '''
        Gets a message with an audio file.
        Returns audio transcription.
        '''
        # Dowload audio file if needed
        file_name, language = self.preprocess(message)
        if self.available:
            self.available = False
            self.bot.reply_to(message, "Procesando audio...")
            try:
                result = self.model.transcribe(audio=file_name, language=language)
                self.reply_transcription(message, result["text"])
            except Exception as e:
                self.bot.reply_to(message, "Ocurrió un error:\n{error}".format(error=e))
            self.available = True
        else:
            self.bot.reply_to(message, "El modelo Whisper está ocupado, inténtelo de nuevo en unos minutos.")
    
    def preprocess(self, message):
        '''
        Gets a message with some type of audio
        Returns file name and language
        '''
        # Get file info
        download_audio = True
        lang = None

        if hasattr(message.voice, "file_id"):
            file_info = self.bot.get_file(message.voice.file_id)
            lang = "es"
        elif hasattr(message.document, "file_id"):
            file_info = self.bot.get_file(message.document.file_id)
        elif hasattr(message.audio, "file_id"):
            file_info = self.bot.get_file(message.audio.file_id)
        elif (message.text[:4] == "http"):
            file_name = message.text
            download_audio = False

        if download_audio:
            downloaded_file = self.bot.download_file(file_info.file_path)
            file_name = f"user_data/{str(message.from_user.id)}.ogg"
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)

        return(file_name, lang)
    
    def reply_transcription(self, message, answer):
        # Manage long answers.
        if (len(answer) < self.longest_message):
            self.bot.reply_to(message, answer)
        else:
            txt_file_name = f"user_data/{str(message.from_user.id)}_transcript.txt"
            with open(txt_file_name, "w") as text_file:
                text_file.write(answer)
            with open(txt_file_name, "r") as text_file:
                self.bot.send_document(message.chat.id, reply_to_message_id=message.message_id,
                                       document=text_file)
