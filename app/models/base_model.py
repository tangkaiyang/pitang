from datetime import datetime

from app.models import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)

    def __init__(self, user):
        self.create_user = user
        self.update_user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
