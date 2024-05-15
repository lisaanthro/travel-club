FROM python:3.11-alpine

WORKDIR /backend

COPY ./backend /backend

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]