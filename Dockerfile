FROM python:3.7

RUN apt-get update

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /anubis

WORKDIR /anubis

RUN pip install -e .

CMD ["python","anubis/reverse_proxy.py"]
