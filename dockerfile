FROM python

RUN pip install openai-whisper pyTelegramBotAPI openai

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /simple_openai_bot

COPY main.py start.txt help.txt prompt.txt /simple_openai_bot/

CMD python main.py
