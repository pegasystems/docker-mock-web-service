FROM python:3.7.6-alpine3.11

RUN pip3 install flask

ADD server.py /server.py

EXPOSE 8080/tcp

CMD ["python", "/server.py"]