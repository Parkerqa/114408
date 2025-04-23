FROM python:3.10

WORKDIR /app

COPY set_webhook.py ./

RUN pip install requests

CMD ["python", "set_webhook.py"]