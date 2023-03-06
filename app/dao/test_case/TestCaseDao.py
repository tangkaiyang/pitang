from app import pitang
from app.models import db
from app.models.test_case import TestCase
from app.utils.logger import Log
from datetime import datetime

from collections import defaultdict


class TestCaseDao(object):
    log = Log("TestCaseDao")

    @staticmethod
    def list_test_case(project_id):
        try:
            case_list = TestCase.query.filter_by(
                project_id=project_id, deleted_at=None).order_by(TestCase.name.asc()).all()
            return TestCaseDao.get_tree(case_list), None
        except Exception as e:
            msg = f"获取测试用例失败:{str(e)}"
            TestCaseDao.log.error(msg)
            return [], msg

    @staticmethod
    def get_tree(case_list):
        result = defaultdict(list)
        # 获取目录->用例的映射关系
        for cs in case_list:
            result[cs.catalogue].append(cs)
        keys = sorted(result.keys())
        # todo title空解决
        tree = [dict(key=f"cat_{key}", children=[{"key": f"case_{child.id}", "title": child.name}
                     for child in result[key]], title=key, total=len(result[key])) for key in keys]
        return tree

    @staticmethod
    def insert_test_case(test_case, user):
        """新增用例

        Args:
            test_case (TestCase): 测试用例
            user (int): 创建人
        """
        try:
            data = TestCase.query.filter_by(name=test_case.get(
                "name"), project_id=test_case.get("project_id"), deleted_at=None).first()
            if data is not None:
                return "用例名称重复"
            cs = TestCase(**test_case, create_user=user)
            db.session.add(cs)
            db.session.commit()
        except Exception as e:
            msg = f"添加用例失败:{str(e)}"
            TestCaseDao.log.error(msg)
            return msg
        return None
