import json
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import MetaData, Table, desc, inspect
from sqlalchemy.orm import Query, Session

from db.base_model import BaseModel as AppBaseModel
from db.session import engine

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

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, offset: Optional[int] = 0, limit: Optional[int] = 100
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .order_by(self.model.created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

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

    def get_query_order_by(
        self, query: Query, order_by: str, asc: bool = True
    ) -> Query:
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
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        updated_by: str,
    ) -> ModelType:
        obj_data = db_obj.dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        history_table_name = f"{self.model.__name__.lower()}history"
        if inspect(engine).has_table(history_table_name):
            engine.execute(
                Table(history_table_name, MetaData(bind=engine), autoload=True)
                .insert()
                .values(
                    obj_id=str(db_obj.id),
                    previous_data=str(obj_data),
                    current_data=str(json.dumps(db_obj)),
                    updated_by=updated_by,
                    created_date=datetime.utcnow(),
                    updated_date=datetime.utcnow(),
                )
            )
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
