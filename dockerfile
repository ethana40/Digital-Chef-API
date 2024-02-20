FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENV OPENAI_API_KEY="Your_OpenAI_API_Key_Here"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
