FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10001:10001
CMD ["uvicorn", "main:app", "--env-file", ".env", "--app-dir", "src" , "--port", "10001", "--host", "0.0.0.0"]
