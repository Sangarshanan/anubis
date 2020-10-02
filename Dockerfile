FROM python:3.7

RUN apt-get update

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /anubis

WORKDIR /anubis

CMD ["python","anubis/serve.py"]

EXPOSE 9000
