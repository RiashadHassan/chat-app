# official slim Python runtime
FROM python:3.12-slim

# don’t write .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# create a user with UID and GID matching host
ARG UID=1000
ARG GID=1000
RUN addgroup --gid $GID appgroup && \
    adduser --disabled-password --gecos "" --uid $UID --gid $GID appuser

# set workdir
WORKDIR /app

# copy and install dependencies
COPY docker/projectile/requirements/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
# copy project code
COPY projectile/ /app/projectile/
# make sure /app is in PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"


# set workdir to projectile directory because manage.py is there
WORKDIR /app/projectile
# collect static files during build
RUN python manage.py collectstatic --noinput

COPY docker/projectile/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# switch to non-root user
USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8000
