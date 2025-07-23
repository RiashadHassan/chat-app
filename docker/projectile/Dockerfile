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

# install dependencies
WORKDIR /app
COPY docker/projectile/requirements/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# set the working dir to where manage.py lives
WORKDIR /app/projectile

# copy the contents of the projectile directory into the container, so that it can be used inside the container
COPY projectile/ /app/projectile/

# execute the entrypoint script
COPY docker/projectile/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# switch to non-root user
USER appuser

EXPOSE 8000
