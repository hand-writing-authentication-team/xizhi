FROM python:2.7.16-stretch

RUN mkdir -p /opt/xizhi
ADD . /opt/xizhi

WORKDIR /opt/xizhi

RUN pip install -r requirements.txt

WORKDIR /opt/xizhi/Handwriting-Authentication-System
RUN pip install -r requirements.txt

WORKDIR /opt/xizhi

CMD ["python", "server.py"]