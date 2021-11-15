FROM python:3.9-slim
WORKDIR /app

RUN apt update

COPY requirements.txt requirements.txt
COPY api-rest-cda.py api-rest-cda.py
COPY modelo_entrega2.pkl modelo_entrega2.pkl
RUN pip3 install -r requirements.txt

EXPOSE 5050
CMD ["python", "api-rest-cda.py"]