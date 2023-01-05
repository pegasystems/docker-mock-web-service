FROM python:3.12.0a3-slim

RUN pip3 install flask requests pg8000 gevent prometheus-flask-exporter

ADD server.py /server.py

EXPOSE 8080/tcp
EXPOSE 8089/tcp

CMD ["python", "/server.py"]