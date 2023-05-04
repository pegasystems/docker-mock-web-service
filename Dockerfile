FROM python:3.11.3-alpine3.17

RUN pip3 install flask requests pg8000 gevent prometheus-flask-exporter
RUN python -m pip uninstall pip -y
ADD server.py /server.py

EXPOSE 8080/tcp
EXPOSE 8089/tcp

CMD ["python", "/server.py"]