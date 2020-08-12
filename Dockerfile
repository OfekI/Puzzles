FROM python:3.8-slim-buster

COPY src /
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
ENTRYPOINT [ "python", "./main.py" ]