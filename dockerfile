FROM python:3.11.2

RUN pip install openai==0.28.0 openai-whisper==20230918 pyTelegramBotAPI==4.13.0

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /simple_openai_bot

COPY main.py start.txt help.txt prompt.txt /simple_openai_bot/

LABEL name=simple_openai_bot

LABEL version=0.3.4

CMD python main.py
