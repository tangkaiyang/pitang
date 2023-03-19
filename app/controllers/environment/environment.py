from flask import Blueprint, jsonify, request

from app import pitang
from app.dao.environment.EnvironmentDao import EnvironmentDao
from app.handler.factory import ResponseFactory
from app.utils.decorator import permission

# 通过Blueprint注册到flask
env = Blueprint("environment", __name__, url_prefix="/environment")


# 定义路径


@env.route("/list")
@permission()
def list_environments(user_info):
    """获取环境列表

    Args:
        user_info (dict): 用户信息
    """
    result, err = EnvironmentDao.list_env(
        request.args)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=ResponseFactory.model_to_list(result), msg="操作成功"))


@env.route("/add", methods=["POST"])
@permission()
def add_environment(user_info):
    """
    新建环境
    :param user_info:
    :return:
    """
    err = EnvironmentDao.insert_env(request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))


@env.route("/update", methods=["POST"])
@permission()
def update_environment(user_info):
    """
    更新环境
    :param user_info:
    :return:
    """
    err = EnvironmentDao.update_env(request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))


@env.route("/delete", methods=["POST"])
@permission()
def delete_environment(user_info):
    """
    删除环境
    :param user_info:
    :return:
    """

    err = EnvironmentDao.delete_env(request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))
