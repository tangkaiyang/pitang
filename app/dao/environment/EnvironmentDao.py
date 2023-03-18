from app.models import db
from app.models.environment import Environment
from app.utils.logger import Log


class EnvironmentDao(object):
    log = Log("EnvironmentDao")

    @staticmethod
    def insert_env(data, user):
        try:
            query = Environment.query.filter_by(name=data.name, deleted_at=None).first()
            if query is not None:
                return f"环境{data.name}已存在"
            env = Environment(data.name, data.remarks, user=user)
            db.session.add(env)
            db.session.commit()
        except Exception as e:
            msg = f"新增环境:{data.name}失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def delete_env(data, user):
        try:
            query = Environment.query.filter_by(id=data.id, deleted_at=None).first()
            if query is None:
                return f"环境{data.name}不存在"
            query.deleted_at = True
            query.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"删除环境:{data.name}失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def update_env(data, user):
        try:
            query = Environment.query.filter_by(name=data.name, deleted_at=None).first()
            if query is not None:
                return f"环境{data.name}已存在"
            env = Environment.query.filter_by(id=data.id, deleted_at=None).first()
            if env is None:
                return f"环境{data.name}不存在"
            env.name = data.name
            env.remarks = data.remarks
            env.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"更新环境:{data.name}失败,{e}"
            EnvironmentDao.log.error(msg)
            return msg

    @staticmethod
    def list_env(data):
        try:
            search_term = data.get("name", "")
            environments = Environment.query.filter(Environment.name.like('%{}%'.format(search_term))).all()
            return environments, None
        except Exception as e:
            msg = f"查询失败,{e}"
            EnvironmentDao.log.error(msg)
            return [], msg
