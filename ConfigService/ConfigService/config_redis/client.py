import redis
import json
from django.conf import settings


class RedisClient:
    def __init__(self):
        self._pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT,db=0 )
        self.client = redis.Redis(connection_pool=self._pool)

    def set_data(self, key, value):
        return self.client.set(key, value)

    def hset_data(self,name,version,value):
        return self.client.hset(name=name,key=version,value=value)

    def get_data(self, key):
        return self.client.get(key)


redis_cli = RedisClient()