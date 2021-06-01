FROM python:3.9.4-slim-buster@sha256:d392dc22fd04662597e6c8fe00744e8a285c47255360f3b12ec410238d31e74a
RUN mkdir /src
RUN mkdir /logs

COPY server.py /src/server.py
ADD _dependencies /usr/local/lib/python3.9/site-packages

EXPOSE 9000/tcp

CMD ["python", "-u", "/src/server.py"]
