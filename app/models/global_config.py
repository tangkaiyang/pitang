from app.models import db
from app.models.base_model import BaseModel
from sqlalchemy import UniqueConstraint


class GlobalConfig(BaseModel):
    id = db.Column(db.INT, primary_key=True)
    env_id = db.Column(db.INT)
    key = db.Column(db.String(16))
    value = db.Column(db.Text)
    key_type = db.Column(db.INT, nullable=False,
                         comment="0:string 1: json 2:yaml")
    enable = db.Column(db.BOOLEAN, default=True)

    __table_args__ = (UniqueConstraint('env_id', 'key', 'deleted_at'),)

    def __init__(self, env_id, key, value, key_type, enable,  user, id=0):
        super().__init__(user)

        self.id = id
        self.env_id = env_id
        self.key = key
        self.value = value
        self.key_type = key_type
        self.enable = enable
