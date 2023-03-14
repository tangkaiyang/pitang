from flask_sqlalchemy import SQLAlchemy

from app import pitang
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

db = SQLAlchemy(pitang)

# 数据库模型,model,操作数据库

# Mysql的session过期时间30min,sqlalchemy默认无过期时间


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
Session = sessionmaker(engine)

# 创建对象的基类
Base = declarative_base()

def update_model(dist, source, update_user=None, not_null=False):
    """
    通过setattr把Form表单的内容赋予这个数据库对象
    :param dist: 被修改对象
    :param source: Pydantic的BaseModel
    :param update_user: 由于我们的每条数据都带有这个updated_at, update_user信息，所以在update的时候我们自动设置为当前时间
    :param not_null: 可选参数，如果是True的话，那么只有非空字段会被更新，这点借鉴了gorm
    :return:
    """
    for var, value in vars(source).items():
        if not_null:
            if value:
                setattr(dist, var, value)
        else:
            setattr(dist, var, value)
        if update_user:
            setattr(dist, 'update_user', update_user)
        setattr(dist, 'update_at', datetime.now())