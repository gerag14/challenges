FROM python:3.10.4-slim-buster

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Install the required packages
RUN pip install --upgrade pip
RUN poetry install

# Run the script
ENTRYPOINT ["/app/entrypoint"]
