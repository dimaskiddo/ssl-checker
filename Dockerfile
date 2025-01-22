FROM python:3.11-alpine
MAINTAINER Dimas Restu Hidayanto <dimas.restu@student.upi.edu>

LABEL maintainer="Dimas Restu Hidayanto <dimas.restu@student.upi.edu>"

WORKDIR /usr/src/app

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=Asia/Jakarta \
    HOME=/

RUN apk --no-cache --update \
      upgrade \
    && apk add --no-cache --update \
        tzdata \
        ca-certificates \
        net-tools \
        bind-tools \
        netcat-openbsd \
        rsync \
        wget

RUN pip3 install --no-cache-dir --break-system-packages --upgrade \
      pip \
      setuptools \
      wheel \
      uv

COPY . ./

RUN pip3 install --no-cache-dir --break-system-packages -r \
      requirements.txt

CMD ["python3", "main.py"]
