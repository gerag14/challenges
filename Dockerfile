FROM python:3.10.4-slim-buster

WORKDIR /app

ENV PYTHONPATH=/app

# Copy the current directory contents into the container at /app
COPY ./src /app
COPY poetry.lock /app
COPY pyproject.toml /app

# Update pip
RUN pip install --upgrade pip

# Install the required packages
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Run the script
COPY ./entrypoint.sh /
RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["tail", "-f", "/dev/null"]
# ENTRYPOINT ["/entrypoint.sh"]
