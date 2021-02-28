FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --upgrade

COPY . /app/

EXPOSE 80

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]