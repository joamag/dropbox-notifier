FROM hivesolutions/python:latest

LABEL version="1.0"
LABEL maintainer="João Magalhães <joamag@gmail.com>"

EXPOSE 8080

VOLUME /data

ENV LEVEL INFO
ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080
ENV FORCE_SSL 1
ENV MONGOHQ_URL mongodb://localhost

ADD requirements.txt /
ADD extra.txt /
ADD src /src

RUN pip3 install -r /requirements.txt && pip3 install -r /extra.txt && pip3 install --upgrade netius

CMD ["/usr/bin/python3", "/src/dropbox_notifier/main.py"]