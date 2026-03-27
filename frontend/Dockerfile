FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py ./app.py
COPY ./config ./config
COPY ./exception ./exception
COPY ./public ./public
COPY ./services ./services
COPY ./utils ./utils
COPY ./.chainlit ./.chainlit

# COPY .env.production .env.production

EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]