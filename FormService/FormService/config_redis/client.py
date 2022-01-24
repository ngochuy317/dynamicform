import redis
import json
from ..default_settings import DEFAULT_SETTINGS,REDIS_HOST,REDIS_PORT


class RedisClient:
    def __init__(self):
        self._pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,
                                          decode_responses=True, db=0 )
        self.client = redis.Redis(connection_pool=self._pool)

    def set_data(self, key, value):
        return self.client.set(key, value)

    def get_data(self, key):
        return self.client.get(key)

    # def get_config(self, key, config_key='form_service'):
    #     configs = json.loads(self.client.get(config_key))
    #     if isinstance(configs,dict):
    #         if key in configs:
    #             return configs[key]
    #     else:
    #         return DEFAULT_SETTINGS[key]

    def get_config(self, key, version='v1.1',config_name='form_service'):
        configs = json.loads(self.client.hget(config_name,version))
        if isinstance(configs,dict):
            if key in configs:
                return configs[key]
        else:
            return DEFAULT_SETTINGS[key]

redis_cli = RedisClient()