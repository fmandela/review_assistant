FROM python:3.7.8-slim

ENV PORT $PORT
ENV MONGO_URL $MONGO_URL

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY . /app

WORKDIR /app

RUN useradd demo
USER demo

CMD ["bash", "/app/bin/run.sh"]