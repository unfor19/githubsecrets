FROM python:3.6.7-slim
WORKDIR /code
RUN pip install --upgrade pip && pip install githubsecrets
ENTRYPOINT [ "ghs" ]
