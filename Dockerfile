FROM python:3.11-bookworm AS base

RUN apt update && apt install -y default-mysql-client
ENV APP_HOME=/src
ENV APP_USER=appuser
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN groupadd -r $APP_USER && \
    useradd -r -g $APP_USER -d $APP_HOME -s /sbin/nologin -c "Docker image user" $APP_USER

WORKDIR $APP_HOME

ENV TZ='Europe/Tallinn'
RUN echo $TZ > /etc/timezone && apt-get update && \
    apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

RUN pip install --upgrade pip setuptools
RUN pip install gunicorn

ADD requirements.txt $APP_HOME
ADD pyproject.toml $APP_HOME
RUN pip install -r requirements.txt

ADD . $APP_HOME


RUN chown -R $APP_USER:$APP_USER $APP_HOME
USER $APP_USER



