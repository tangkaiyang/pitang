# from datetime import datetime
#
# from app.models import db
#
#
# class BaseModel(db.Model):
#     created_at = db.Column(db.DATETIME, nullable=False)
#     updated_at = db.Column(db.DATETIME, nullable=False)
#     deleted_at = db.Column(db.DATETIME)
#     create_user = db.Column(db.INT, nullable=True)
#     update_user = db.Column(db.INT, nullable=True)
#
#     def __init__(self, user):
#         self.create_user = user
#         self.update_user = user
#         self.created_at = datetime.now()
#         self.updated_at = datetime.now()

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_user = Column(String(100))
    update_user = Column(String(100))
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self, deleted_by):
        self.deleted_at = datetime.utcnow()
        self.update_user = deleted_by

    def update_fields(self, updated_by, **fields):
        for key, value in fields.items():
            setattr(self, key, value)
        self.update_user = updated_by
        self.update_at = datetime.utcnow()

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, create_at={self.create_at}, update_at={self.update_at}, create_user={self.create_user}, update_user={self.update_user}, deleted_at={self.deleted_at})>"
