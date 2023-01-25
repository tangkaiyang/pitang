from flask_sqlalchemy import SQLAlchemy

from app import pitang

db = SQLAlchemy(pitang)

# 数据库模型,model,操作数据库