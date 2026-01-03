# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10 AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN <<EOF
apt-get update
apt-get install -y git
EOF

RUN <<EOF
groupadd docker
useradd -m -s /bin/bash -g docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /