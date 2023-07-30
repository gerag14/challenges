from pydantic import BaseModel


class SchemaImportFileBase(BaseModel):
    file_name: str
    bucket_name: str


class SchemaImportFileCreate(SchemaImportFileBase):
    pass


class SchemaImportFileUpdate(BaseModel):
    processed: bool


class SchemaImportFile(SchemaImportFileBase):
    id: int

    class Config:
        orm_mode = True
