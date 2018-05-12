FROM python:3.6
WORKDIR /usr/src/app

RUN apt-get install fontconfig
COPY requirements.txt requirements_dev.txt requirements.lock ./
ARG UPDATE_LOCK
RUN if [ -z "$UPDATE_LOCK" ]; then pip install --no-cache-dir -r requirements.lock; fi
RUN pip install --no-cache-dir -r requirements.txt
ARG DEPENDENCIES
RUN if [ ! -z "$DEPENDENCIES" ]; then pip install -r $DEPENDENCIES; fi
COPY src/ ./
