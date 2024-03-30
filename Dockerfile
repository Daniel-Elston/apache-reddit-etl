FROM python:3.12.2-slim

WORKDIR /apache-reddit-live

# Copy your application code and requirements.txt into the container
COPY . /apache-reddit-live

# Install Python dependencies
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
