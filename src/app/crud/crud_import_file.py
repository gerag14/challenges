from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.import_file import ImportFile
from app.schemas.schema_import_file import SchemaImportFileCreate, SchemaImportFileUpdate

from .crud_base import CRUDBase


class CRUDImportFile(CRUDBase[ImportFile, SchemaImportFileCreate, SchemaImportFileUpdate]):
    def get_by_name_bucket(self, db: Session, *, file_name: str, bucket_name: str) -> Optional[ImportFile]:
        return (
            db.query(ImportFile)
            .filter(
                func.lower(ImportFile.file_name) == file_name.lower(),
                func.lower(ImportFile.bucket_name) == bucket_name.lower(),
            )
            .first()
        )


crud_import_file = CRUDImportFile(ImportFile)
