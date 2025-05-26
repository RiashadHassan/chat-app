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

# in dev the volume mount overrides this, so it’s harmless:
COPY projectile/ /app/projectile/

# switch to non-root user
USER appuser

EXPOSE 8000

# Default command – will run in /app/projectile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
