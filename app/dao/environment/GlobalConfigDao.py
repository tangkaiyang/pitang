from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.sql.functions import count

from app.models import db
from app.models.environment import Environment
from app.models.global_config import GlobalConfig
from app.utils.logger import Log


class GlobalConfigDao(object):
    log = Log("GlobalConfigDao")

    @staticmethod
    def insert_global_config(data, user):
        try:
            env_id, key, value, key_type, enable = data.get("env_id"), data.get("key"), data.get("value"), data.get(
                "key_type"), data.get("enable")
            query = Environment.query.filter_by(
                id=env_id, deleted_at=None).first()
            if query is None:
                return "环境不存在"
            query_config = GlobalConfig.query.filter_by(
                id=env_id, key=key, deleted_at=None).first()
            if query_config is not None:
                return f"全局变量{key}已存在"
            global_config = GlobalConfig(
                env_id, key, value, key_type, enable, user)
            db.session.add(global_config)
            db.session.commit()
        except Exception as e:
            msg = f"新增全局变量:{key}失败,{e}"
            GlobalConfigDao.log.error(msg)
            return msg

    @staticmethod
    def delete_global_config(data, user):
        try:
            config_id = data.get("id")
            query = GlobalConfig.query.filter_by(
                id=config_id, deleted_at=None).first()
            if query is None:
                return f"全局变量不存在"
            query.deleted_at = datetime.now()
            query.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"删除全局变量失败,{e}"
            GlobalConfigDao.log.error(msg)
            return msg

    @staticmethod
    def update_global_config(data, user):
        try:
            # todo request属性复制给dao
            update_id, env_id, key, value, key_type, enable = data.get("id"), data.get("env_id"), data.get(
                "key"), data.get("value"), data.get(
                "key_type"), data.get("enable")
            query = Environment.query.filter_by(
                id=env_id, deleted_at=None).first()
            if query is None:
                return "环境不存在"
            query_config = GlobalConfig.query.filter_by(
                id=env_id, key=key, deleted_at=None).first()
            if query_config is None:
                return f"全局变量{key}不存在"
            # todo request属性复制给数据行
            query_config.env_id = env_id
            query_config.key = key
            query_config.value = value
            query_config.key_type = key_type
            query_config.enable = enable
            query_config.update_user = user
            query_config.updated_at = datetime.now()
            db.session.commit()
        except Exception as e:
            msg = f"更新全局变量失败,{e}"
            GlobalConfigDao.log.error(msg)
            return msg

    @staticmethod
    def list_global_config(data):
        try:
            search_term = data.get("key", "")
            # todo 补充排序,分页
            configs = GlobalConfig.query.filter_by(deleted_at=None).filter(
                GlobalConfig.key.like('%{}%'.format(search_term))).all()
            total = count(configs)
            return configs, total, None
        except Exception as e:
            msg = f"查询失败,{e}"
            GlobalConfigDao.log.error(msg)
            return [], 0, msg
