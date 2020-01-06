FROM python:3

COPY ./* /v2rayui
RUN apt update && apt install -y cron && apt clean all && cd /v2rayui && pip install -r requirements.txt
WORKDIR /v2rayui

EXPOSE 8080

ENTRYPOINT ["python3", "manage.py", "crontab", "add"]
CMD [ "gunicorn", "-w", "6", "-k", "gevent", "-b", "0.0.0.0:8080", "wsgi:application" ]
