FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt

COPY app.py .
COPY static/upload.html upload.html
COPY static/style.css style.css
COPY static/upload.js upload.js

EXPOSE 8000

CMD ["python", "app.py"]