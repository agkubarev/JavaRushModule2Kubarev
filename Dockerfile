FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt

COPY app.py .
COPY static/upload.html upload.html
COPY static/style.css style.css
COPY static/upload.js upload.js
COPY db/queries/init_tables.sql db/queries/init_tables.sql
COPY db/DBManager.py db/DBManager.py
COPY ImageHostingHandler.py ImageHostingHandler.py
COPY settings.py settings.py

EXPOSE 8000

CMD ["python", "app.py"]