FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Avvia il server Flask
#CMD ["python3","-m","flask", "run", "--host=0.0.0.0"]
CMD ["python3", "app.py"]