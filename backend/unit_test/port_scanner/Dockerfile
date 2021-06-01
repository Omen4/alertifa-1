FROM python:3.9.4-slim-buster@sha256:d392dc22fd04662597e6c8fe00744e8a285c47255360f3b12ec410238d31e74a
RUN mkdir /src

COPY port_scanner.py /src/port_scanner.py

# COPY requirements.txt /src/requirements.txt
# RUN pip3 install -r /src/requirements.txt

CMD ["python", "-u", "/src/port_scanner.py"]
