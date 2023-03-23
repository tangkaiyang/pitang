from pydantic import BaseModel, validator
from app.exceptions.ParamsException import ParamsError


class GlobalConfig(BaseModel):
    id: int = None
    key: str
    value: str
    env_id: int = None
    key_type: int
    enable: bool

    @validator("key", "name", "key_type", "enable")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError('不能为空')
        if not v:
            raise ParamsError("不能为空")
        return v
