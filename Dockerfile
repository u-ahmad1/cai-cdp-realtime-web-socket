FROM python:3.9.17-slim
RUN pip3 install -r requirements.txt
EXPOSE 8005:8005
RUN python3 ReadFromKafka.py
