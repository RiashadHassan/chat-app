# use slim Python base
FROM python:3.12-slim

# avoid writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# set working directory and copy requirements
WORKDIR /app
COPY docker/chat_service/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# copy application source
COPY chat_service/app /app/app

# set working dir where main.py lives
WORKDIR /app/app

EXPOSE 9000

# uvicorn dev server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
