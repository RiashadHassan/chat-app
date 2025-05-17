# official slim Python runtime
FROM python:3.12-slim

# don’t write .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install dependencies
WORKDIR /app
COPY docker/requirements/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# set the working dir to where manage.py lives
WORKDIR /app/projectile

# in dev the volume mount overrides this, so it’s harmless:
COPY projectile/ /app/projectile/

EXPOSE 8000

# Default command – will run in /app/projectile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
