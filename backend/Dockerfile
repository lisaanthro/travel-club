FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]