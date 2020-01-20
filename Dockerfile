FROM python:3

COPY ./ /v2rayui/
RUN cd /v2rayui && pip install -r requirements.txt
WORKDIR /v2rayui

EXPOSE 8080

CMD [ "gunicorn", "-w", "6", "-k", "gevent", "-b", "0.0.0.0:8080", "wsgi:application" ]
