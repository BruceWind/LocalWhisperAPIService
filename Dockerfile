FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# RUN pip install -r requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]