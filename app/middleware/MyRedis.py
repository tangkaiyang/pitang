import redis


class MyRedis:
    def __init__(self, host='localhost', port=6379, db=0):
        self.conn = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.conn.set(key, value)

    def get(self, key):
        return self.conn.get(key)

    def delete(self, key):
        self.conn.delete(key)

    def update(self, key, value):
        if self.conn.exists(key):
            self.conn.set(key, value)
        else:
            raise KeyError(f"Key '{key}' does not exist in Redis")

# 使用示例
if __name__ == "__main__":
    my_redis = MyRedis()
    
    # 设置键值对
    my_redis.set('mykey:inner', 'myvalue:inner')
    my_redis.set('mykey:inner', '111111')
    
    # 获取值
    value = my_redis.get('mykey')
    print(value.decode())  # 输出 'myvalue'
    
    # 更新值
    my_redis.set('mykey:inner', 'newvalue')
    updated_value = my_redis.get('mykey')
    print(updated_value.decode())  # 输出 'newvalue'
    
    # 删除键
    # my_redis.delete('mykey')
    deleted_value = my_redis.get('mykey')
    print(deleted_value)  # 输出 None
