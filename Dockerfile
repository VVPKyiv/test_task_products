# Use the official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /usr/src

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
RUN mkdir logs
RUN touch logs/celery.log
# Copy the current directory contents into the container
COPY . .

# Command to run on container start
#CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
CMD ["ls", ""]

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]