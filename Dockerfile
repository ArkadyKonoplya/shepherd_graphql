# Use official Python image from Docker Hub
FROM python:3.9

ARG APP_USER=appuser
ARG aws_ses_access_key_id
ARG aws_ses_secret_access_key
ARG aws_s3_storage_bucket_name
ARG darksky_api_key
ARG DATABASE_ENGINE
ARG db_host
ARG db_password
ARG db_port
ARG db_username
ARG default_from_email
ARG django_secret_key
ARG fcm_server_key
ARG google_maps_api_key
ARG PRIMARY_DOMAIN
ARG DJSTRIPE_FOREIGN_KEY_TO_FIELD
ARG DJSTRIPE_USE_NATIVE_JSONFIELD
ARG DJSTRIPE_WEBHOOK_SECRET
ARG STRIPE_LIVE_MODE
ARG STRIPE_LIVE_PUBLIC_KEY
ARG STRIPE_LIVE_SECRET_KEY
ARG STRIPE_TEST_PUBLIC_KEY
ARG STRIPE_TEST_SECRET_KEY
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN set -ex \
    && RUN_DEPS="\
    libpcre3 \
    mime-support \
    postgresql-client \
    binutils \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{}\
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# These env variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Make a new directory to put our code in.
RUN mkdir /code

# Change the working directory.
# Every command after this will be run from the /code directory.
WORKDIR /code

# Copy the requirements.txt file

COPY ./Pipfile /code/
#COPY ./Pipfile.lock /code/

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    python3-dev \
    libpcre3-dev \
    libproj-dev \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --system --deploy --skip-lock\
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code.
ADD . /code/

#uWSGI will listen on this port
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=shepherd.settings.base
ENV UWSGI_WSGI_FILE=shepherd/wsgi.py
# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

ENV PRIMARY_DOMAIN=$PRIMARY_DOMAIN STRIPE_TEST_SECRET_KEY=$STRIPE_TEST_SECRET_KEY STRIPE_TEST_PUBLIC_KEY=$STRIPE_TEST_PUBLIC_KEY STRIPE_LIVE_SECRET_KEY=$STRIPE_LIVE_SECRET_KEY STRIPE_LIVE_PUBLIC_KEY=$STRIPE_LIVE_PUBLIC_KEY STRIPE_LIVE_MODE=$STRIPE_LIVE_MODE DJSTRIPE_WEBHOOK_SECRET=$DJSTRIPE_WEBHOOK_SECRET DJSTRIPE_USE_NATIVE_JSONFIELD=$DJSTRIPE_USE_NATIVE_JSONFIELD DJSTRIPE_FOREIGN_KEY_TO_FIELD=$DJSTRIPE_FOREIGN_KEY_TO_FIELD aws_ses_access_key_id=$aws_ses_access_key_id aws_ses_secret_access_key=$aws_ses_secret_access_key darksky_api_key=$darksky_api_key DATABASE_ENGINE=$DATABASE_ENGINE db_host=$db_host db_password=$db_password db_port=$db_port db_username=$db_username django_secret_key=$django_secret_key fcm_server_key=$fcm_server_key aws_s3_storage_bucket_name=$aws_s3_storage_bucket_name default_from_email=$default_from_email

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--worker-class", "gthread", "shepherd.wsgi:application"]