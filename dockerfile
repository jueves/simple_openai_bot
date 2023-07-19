FROM python

RUN pip install pyTelegramBotAPI openai openai-whisper

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /simple_openai_bot

COPY main.py start.txt help.txt /simple_openai_bot/

CMD python main.py
