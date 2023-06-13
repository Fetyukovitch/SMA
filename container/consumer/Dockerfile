FROM tensorflow/tensorflow:2.10.0

WORKDIR /opt/

COPY consumer/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY consumer ./consumer


EXPOSE 8000
ENV PORT=8000

WORKDIR /opt/consumer/

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
