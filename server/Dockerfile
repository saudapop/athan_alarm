FROM python:3.7.7-slim-buster

WORKDIR /app

RUN apt update && apt upgrade;
RUN echo y | apt install curl;
RUN  rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/$(curl https://ipapi.co/timezone) /etc/localtime;

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
