FROM python:3.8.8

RUN pip install --upgrade pip
COPY requirment.txt  .
RUN pip install --no-cache-dir -r  requirements.txt
