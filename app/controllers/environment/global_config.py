from flask import Blueprint, jsonify, request

from app import pitang
from app.dao.environment.GlobalConfigDao import GlobalConfigDao
from app.dao.environment.GlobalConfigDao import GlobalConfig
from app.handler.factory import ResponseFactory
from app.utils.decorator import permission

# 通过Blueprint注册到flask
gconfig = Blueprint("gconfig", __name__, url_prefix="/environment/gconfig")


# 定义路径


@gconfig.route("/list")
@permission()
def list_global_configs(user_info):
    """获取全局变量列表

    Args:
        user_info (dict): 用户信息
    """
    result, total, err = GlobalConfigDao.list_global_config(
        request.args)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=ResponseFactory.model_to_list(result), msg="操作成功"))


@gconfig.route("/add", methods=["POST"])
@permission()
def add_global_config(user_info):
    """
    新建全局变量
    :param user_info:
    :return:
    """
    err = GlobalConfigDao.insert_global_config(
        request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))


@gconfig.route("/update", methods=["POST"])
@permission()
def update_global_config(user_info):
    """
    更新全局变量
    :param user_info:
    :return:
    """
    err = GlobalConfigDao.update_global_config(
        request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))


@gconfig.route("/delete", methods=["POST"])
@permission()
def delete_global_config(user_info):
    """
    删除全局变量
    :param user_info:
    :return:
    """

    err = GlobalConfigDao.delete_global_config(
        request.get_json(), user_info.get("id"))
    if err is not None:
        return jsonify(dict(code=110, data=None, msg=err))
    return jsonify(dict(code=0, data=None, msg="操作成功"))
