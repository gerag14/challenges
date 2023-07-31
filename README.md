# Project Stori Challenges

## Description

The project aims to process and summarize transaction data and account information.
The code is implemented in Python. The code uses a Docker image and docker-compose to compile and run the code.

## Prerequisites

- Git
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

- Change enviroments variables:

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

1. Run docker compose

   ```bash
   docker-compose up -d
   ```

2. Run program

- Local:

  ```bash
  ./execute run
  ```

- aws:

  ```bash
  ./execute run_aws
  ```

## Tests

### To run tests

```bash
./execute tests
```

## Developers

### Folder structure

<pre>
project/
│
├── app/
│   ├── main.py
│   ├── crud/
│   │   ├── crud_transaction.py
│   │   ├── crud_account.py
│   │   └── crud_importfile.py
│   ├── models/
│   │   ├── transaction.py
│   │   ├── account.py
│   │   └── importfile.py
│   ├── schemas/
│   │   ├── transaction_schema.py
│   │   ├── account_schema.py
│   │   └── importfile_schema.py
│   ├── core/
│   │   ├── import_transactions.py
│   │   ├── notify_transactions_summary.py
│   │   └── transactions_summary.py
│   ├── services/
│   │   ├── aws_service.py
│   │   └── email_service.py
│   ├── tests/
│   │   └── all pytest tests
│
├── db/
│   └── files DB config & base models
│
├── static/
│   └── public_files
│
├── static_root/
│   └── private_files
│
├── alembic/
│   └── Manager migrations
│
├── .env.example
├── .env
├── README.md
├── execute
│   └── Manage shortcuts commands in entrypoint
</pre>
