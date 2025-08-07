FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./config ./config
COPY ./exception ./exception
COPY ./public ./public
COPY ./services ./services
COPY ./utils ./utils
COPY ./.chainlit ./.chainlit

COPY .env.production .env.production

EXPOSE 8123

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8123"]