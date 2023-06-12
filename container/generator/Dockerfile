FROM tensorflow/tensorflow:2.10.0
#FROM python:3.10.10-slim

WORKDIR /opt/

COPY generator/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

 #COPY setup.py .
COPY generator ./generator

#RUN pip install .

EXPOSE 8000
ENV PORT=8000

WORKDIR /opt/generator/

#ENTRYPOINT ["python", "main.py"]
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
