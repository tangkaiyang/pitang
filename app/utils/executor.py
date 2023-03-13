import json
from app.utils.logger import Log
from app.middleware.HttpClient import Request
from app.dao.test_case import TestCaseDao


class Executor(object):
    log = Log("executor")

    @staticmethod
    def run(case_id):
        result = dict()
        try:
            case_info, err = TestCaseDao.query_test_case(case_id)
            if err:
                return result, err
            if case_info.request_header != "":
                headers = json.loads(case_info.request_header)
            else:
                headers = dict()
            if case_info.body != "":
                body = case_info.body
            else:
                body = None
            request_obj = Request(case_info.url, headers=headers, data=body)
            method = case_info.request_method.upper()
            response_info = request_obj.request(method)
            return response_info, None
        except Exception as e:
            msg = f"执行用例失败:{str(e)}"
            Executor.log.error(msg)
            return result, msg
