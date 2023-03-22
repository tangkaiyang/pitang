from app.models import db
from app.models.user import User
from app.models.test_case import TestCase
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.environment import Environment
from app.models.global_config import GlobalConfig

db.create_all()


# DAO(database access object):数据访问接口
