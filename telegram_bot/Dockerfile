FROM python:3.11

WORKDIR .

COPY requirements.txt requirements.txt

RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . .

CMD ["python3", "bot/bot.py"]