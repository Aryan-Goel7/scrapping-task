FROM python:slim-bookworm

WORKDIR /usr/src/app


RUN apt-get update && \
    apt-get install -y \
        wget \
        gnupg \
        firefox-esr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip


COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
