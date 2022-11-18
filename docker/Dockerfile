FROM python:3.8

ENV SRC_DIR /usr/bin/src/webapp/src

COPY src/* ${SRC_DIR}/

WORKDIR ${SRC_DIR}

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]