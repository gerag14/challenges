from sqlalchemy.orm import Session

from app.crud.crud_import_file import crud_import_file
from app.schemas.schema_import_file import SchemaImportFile, SchemaImportFileCreate
from app.tests.utils import random_lower_string


def create_random_import_file(db: Session) -> SchemaImportFile:
    file_name = random_lower_string()
    bucket_name = random_lower_string()
    import_file_in = SchemaImportFileCreate(file_name=file_name, bucket_name=bucket_name)
    import_file = crud_import_file.create(db=db, obj_in=import_file_in)
    return import_file


def test_create_import_file(db: Session) -> None:
    import_file = create_random_import_file(db=db)
    assert import_file.file_name
    assert import_file.bucket_name
