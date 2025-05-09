FROM ubuntu:22.04
LABEL MAINTAINER="github.com/oregonpillow"

ENV PKGS="python3 python3-serial python3-pip" \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && apt-get dist-upgrade curl -yq \
    && apt-get -yq install --no-install-recommends  ${PKGS} \
    && pip3 install prometheus_client requests

RUN apt-get autoremove -yq \
    && apt-get autoclean \
    && rm -fr /tmp/* /var/lib/apt/lists/*

RUN mkdir -p /opt/temper/bin

COPY temper-exporter.py /opt/temper/bin

EXPOSE 8000

WORKDIR /opt/temper/bin
ENTRYPOINT  ["/opt/temper/bin/temper-exporter.py"]
