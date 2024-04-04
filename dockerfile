FROM python:3.11

WORKDIR /apache-reddit-live

COPY . /apache-reddit-live

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
