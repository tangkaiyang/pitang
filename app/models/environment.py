from app.models import db
from app.models.base_model import BaseModel


class Environment(BaseModel):
    __tablename__ = 'environment'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    remarks = db.Column(db.String(200))

    def __init__(self, name, remarks, user, id=0):
        super(user)
        self.id = id
        self.name = name
        self.remarks = remarks
