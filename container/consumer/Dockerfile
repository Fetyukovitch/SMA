FROM tensorflow/tensorflow:2.10.0
#FROM python:3.10.10-slim

WORKDIR /opt/

COPY consumer/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

 #COPY setup.py .
COPY consumer ./consumer

#RUN pip install .

EXPOSE 8000
ENV PORT=8000

WORKDIR /opt/consumer/

ENTRYPOINT ["python", "main.py"]
#CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
