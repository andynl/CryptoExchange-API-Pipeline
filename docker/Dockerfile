FROM python:3.9.5

WORKDIR /project

RUN apt-get update && apt-get install cron -y nano

COPY ./ /project/

RUN pip install -r requirements.txt

COPY ./schedule/orchestrate_etl /etc/cron.d/orchestrate_etl

RUN chmod 0644 /etc/cron.d/orchestrate_etl

RUN crontab /etc/cron.d/orchestrate_etl

CMD sh /project/docker/commands.sh
