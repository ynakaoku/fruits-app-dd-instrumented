#FROM python:3.5.2
FROM python:3.9 as build

# RUN groupadd web
# RUN useradd -d /home/python -m python

# Env vars for Datadog Instrumentation
ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL} 
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}

RUN mkdir /home/python
WORKDIR /home/python
#ADD index.html .
RUN wget https://raw.githubusercontent.com/ynakaoku/fruits-app-dd-instrumented/main/index.html
#ADD cgiserver.py .
RUN wget https://raw.githubusercontent.com/ynakaoku/fruits-app-dd-instrumented/main/cgiserver.py
#ADD index.html /home/python
RUN mkdir fruits
#ADD db_get.py .
RUN wget https://raw.githubusercontent.com/ynakaoku/fruits-app-dd-instrumented/main/db_get.py
RUN mv db_get.py ./fruits
RUN chmod 755 ./fruits/db_get.py

RUN apt-get -y update
RUN apt-get -y install wget unzip iputils-ping
RUN apt-get -y install python3-pip
RUN python -m pip install pymongo==3.9

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/python", "/home/python/cgiserver.py"]
# USER python
