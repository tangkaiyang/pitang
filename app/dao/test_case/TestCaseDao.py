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
        tree = [dict(key=f"cat_{key}", children=[{"key": f"case_{child.id}", "title": child.name}
                     for cihld in result[key]], title=key, total=len(result[key])) for key in keys]
        return tree
