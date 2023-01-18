'''
变量池
变量生命周期与用例一致
'''


class VarPool(object):
    def __init__(self, case_id) -> None:
        self.cache = dict()
        self.case_id = case_id

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key)

    def get_default(self, key, default_value):
        return self.cache.get(key, default_value)
