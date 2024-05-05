FROM python:3.11-alpine

WORKDIR /backend

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./backend /backend

CMD ["uvicorn", "limehd.main:app", "--host", "0.0.0.0"]