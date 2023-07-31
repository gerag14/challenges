# Project Stori Challenges

## Description

The project aims to process and summarize transaction data and account information.
The code is implemented in Python. The code uses a Docker image and docker-compose to compile and run the code.

## Prerequisites

- Docker

## Setup

1. Clone the repository from GitHub:

   ```bash
   git clone https://github.com/gerag14/challenges.git
   cd challenges
   ```

2. Configuration and run setup:

   ```bash
   ./setup.sh
   ```

### Change enviroments variables:

- SQLALCHEMY_DATABASE_URI
- SMTP_TLS
- SMTP_PORT
- SMTP_HOST
- SMTP_USER
- SMTP_PASSWORD
- EMAILS_FROM_NAME
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION_NAME
- AWS_BUCKET

3. Run docker compose

   ```bash
   docker-compose up -d
   ```

4. Run program

### to run local

```bash
./execute run
```

### to run local aws

```bash
./execute run_aws
```

## Tests

### To run tests

```bash
./execute tests
```
