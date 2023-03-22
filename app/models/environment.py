from app.models import db
from app.models.base_model import BaseModel
from sqlalchemy import UniqueConstraint


class Environment(BaseModel):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(10))
    remarks = db.Column(db.String(200))

    __table_args__ = (UniqueConstraint('name', 'deleted_at'),)

    def __init__(self, name, remarks, user, id=0):
        super().__init__(user)

        self.id = id
        self.name = name
        self.remarks = remarks
