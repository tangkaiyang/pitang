
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
