FROM python:3.6-slim
WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get -y install fontconfig \
    && apt-get -y clean
COPY requirements.txt requirements_dev.txt requirements.lock ./
ARG UPDATE_LOCK
RUN if [ -z "$UPDATE_LOCK" ]; then pip install --no-cache-dir -r requirements.lock; fi
RUN pip install --no-cache-dir -r requirements.txt
ARG DEPENDENCIES
RUN if [ ! -z "$DEPENDENCIES" ]; then pip install -r $DEPENDENCIES; fi
COPY src/ ./
ENV PYTHONPATH $PYTHONPATH:/usr/src/app
