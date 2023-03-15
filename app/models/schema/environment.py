from pydantic import BaseModel, validator
from app.exceptions.ParamsException import ParamsError


class Environment(BaseModel):
    id: int
    name: str
    remarks: str

    @validator('name')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError('不能为空')
        return v
