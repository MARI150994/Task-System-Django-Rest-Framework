FROM python:3.8-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x prestart.sh
ENTRYPOINT ["bash", "prestart.sh"]
