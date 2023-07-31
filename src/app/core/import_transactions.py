import csv
import logging
import os

from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.crud.crud_import_file import crud_import_file
from app.crud.crud_transaction import crud_transaction
from app.schemas.schema_import_file import SchemaImportFile, SchemaImportFileCreate, SchemaImportFileUpdate
from app.schemas.schema_transaction import SchemaTransactionCreate
from app.services.aws_service import AWSService
from db.session import atomic_transaction


class ImportTransactions:
    def __init__(self, db: Session):
        self._db = db
        self.path = "static_root/transactions"

    def import_transactions(self, load_from_boto3=False):
        if load_from_boto3:
            self.import_from_s3()
        self.process_files()

    def import_from_s3(self):
        AWSService().import_s3_files(path=self.path)

    def process_files(self):
        """IMPORT TRANSACTIONS FROM LOCAL CSV FILES IN STATIC_ROOT/TRANSACTIONS"""
        for file_name in os.listdir(self.path):
            if self.__validate_file(file_name):
                file_import = self.__get_file_in_db(file_name)
                # self.process_file(file_import)
                try:
                    self.process_file(file_import)
                except Exception as error:
                    logging.info(f"Error processing file {file_name}: {error}")

    def process_file(self, file_import: SchemaImportFile):
        with open(f"{file_import.bucket_name}/{file_import.file_name}", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            data = list(reader)
            self.load_data_from_csv(file_import, data)

    def load_data_from_csv(self, file_import, data):
        with atomic_transaction(self._db) as atomic:
            for row in data:
                if self.__validate_transaction(row):
                    account = crud_account.get_by_account_number(atomic, account_number=row[1])
                    if account:
                        transaction_in = SchemaTransactionCreate(
                            account_id=account.id,
                            importfile_id=file_import.id,
                            transaction_import_id=row[0],
                            transaction_date=row[2],
                            amount=row[3],
                        )
                    crud_transaction.create(atomic, obj_in=transaction_in)
            crud_import_file.update(atomic, db_obj=file_import, obj_in=SchemaImportFileUpdate(processed=True))

    def __get_file_in_db(self, file_name: str):
        file_in_db = crud_import_file.get_by_name_bucket(db=self._db, file_name=file_name, bucket_name=self.path)
        if file_in_db:
            return file_in_db
        cypto = SchemaImportFileCreate(
            file_name=file_name,
            bucket_name=self.path,
        )
        file_import = crud_import_file.create(self._db, obj_in=cypto)
        return file_import

    def __validate_headers(self, file_name: str) -> bool:
        expected_headers = ["transaction", "account", "date", "amount"]
        with open(f"{self.path}/{file_name}", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            headers = next(reader)

        headers = [header.lower() for header in headers]
        is_valid = len(headers) == 4 and headers == expected_headers
        if not is_valid:
            logging.info(f"File {file_name} has invalid headers")
        return is_valid

    def __validate_file(self, file_name: str) -> bool:
        if not file_name.endswith(".csv"):
            logging.info(f"File {file_name} is not a CSV file")
            return False

        # TODO: validate if file is already processed
        file_in_db = crud_import_file.get_by_name_bucket(db=self._db, file_name=file_name, bucket_name=self.path)
        if file_in_db and file_in_db.processed:
            return False

        if not self.__validate_headers(file_name=file_name):
            return False
        return True

    def __validate_transaction(self, row: list) -> bool:
        if len(row) != 4:
            logging.info(f"Transaction {row[0]} has invalid data")
            raise Exception(f"Transaction {row[0]} has invalid data")

        exists = crud_transaction.get_by_transaction_import_id(self._db, transaction_import_id=row[0])
        if exists:
            logging.info(f"Transaction {row[0]} already exists")
            return False
        return True
