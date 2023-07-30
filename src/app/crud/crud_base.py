from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Query, Session

from db.base_model import BaseModel as AppBaseModel

ModelType = TypeVar("ModelType", bound=AppBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    @classmethod
    def validate_update_schema_type(cls, obj_in: Any) -> None:
        if not isinstance(obj_in, UpdateSchemaType):
            raise ValueError("obj_in must be an instance of UpdateSchemaType")

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, offset: Optional[int] = 0, limit: Optional[int] = 100) -> List[ModelType]:
        return db.query(self.model).order_by(self.model.created_date.desc()).offset(offset).limit(limit).all()

    def get_query_filter_by(
        self,
        db: Optional[Session] = None,
        *,
        filter_by: dict,
        query: Optional[Query] = None,
        ilike: Optional[bool] = False,
    ) -> Query:
        if not query:
            query = db.query(self.model)

        if ilike:
            for attr in [k for k, v in filter_by.items() if v is not None]:
                if attr in self.model.__table__.c.keys():
                    field = getattr(self.model, attr)
                    if "ilike" in dir(field) and attr != "id":
                        query = query.filter(field.ilike(f"%{filter_by[attr]}%"))
                    else:
                        query = query.filter(field == filter_by[attr])
            return query

        for attr in [k for k, v in filter_by.items() if v is not None]:
            if attr in self.model.__table__.c.keys():
                query = query.filter(getattr(self.model, attr) == filter_by[attr])
        return query

    def get_query_order_by(self, query: Query, order_by: str, asc: bool = True) -> Query:
        if order_by in self.model.__table__.c.keys():
            if asc:
                return query.order_by(getattr(self.model, order_by))
            return query.order_by(desc(getattr(self.model, order_by)))
        return query

    def get_query_order_by_related_model(
        self,
        query: Query,
        related_model: Any,
        order_by: str,
        asc: bool = True,
    ) -> Query:
        if asc:
            return query.order_by(getattr(related_model, order_by))
        return query.order_by(desc(getattr(related_model, order_by)))

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        if db._nested_transaction:
            db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        if db._nested_transaction:
            db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.flush()
        return obj
