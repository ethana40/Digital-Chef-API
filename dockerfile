FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

ARG REPO_URL

RUN git clone $REPO_URL /app

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY="Your_OpenAI_API_Key_Here"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]