from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.sql.functions import count

from app.models import db
from app.models.environment import Environment
from app.utils.logger import Log


class EnvironmentDao(object):
    log = Log("EnvironmentDao")

    @staticmethod
    def insert_env(data, user):
        try:
            name, remarks = data.get("name", ""), data.get("remarks", "")
            query = Environment.query.filter_by(name=name, deleted_at=None).first()
            if query is not None:
                return f"环境{name}已存在"
            env = Environment(name, remarks, user=user)
            db.session.add(env)
            db.session.commit()
        except Exception as e:
            msg = f"新增环境:{name}失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def delete_env(data, user):
        try:
            env_id = data.get("id")
            query = Environment.query.filter_by(id=env_id, deleted_at=None).first()
            if query is None:
                return f"环境不存在"
            query.deleted_at = datetime.now()
            query.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"删除环境失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def update_env(data, user):
        try:
            env_id, name, remarks = data.get("id"), data.get("name", ""), data.get("remarks", "")
            query = Environment.query.filter_by(name=name, deleted_at=None).first()
            if query is not None:
                return f"环境{name}已存在"
            env = Environment.query.filter_by(id=env_id, deleted_at=None).first()
            if env is None:
                return f"环境{name}不存在"
            env.name = name
            env.remarks = remarks
            env.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"更新环境失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def list_env(data):
        try:
            search_term = data.get("name", "")
            # todo 补充排序,分页
            environments = Environment.query.filter_by(deleted_at=None).filter(
                or_(Environment.name.like('%{}%'.format(search_term)),
                    Environment.remarks.like('%{}%'.format(search_term)))).all()
            total = count(environments)
            return environments, total, None
        except Exception as e:
            msg = f"查询失败,{e}"
            EnvironmentDao.log.error(msg)
            return [], 0, msg
