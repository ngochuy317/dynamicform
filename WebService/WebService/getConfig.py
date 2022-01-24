import requests
from .default_settings import DEFAULT_SETTINGS

class ConfigAPI:
    def __init__(self):
        self._base_url = "http://configservice:8083/api/web_service/v1.1/"
        self.requests = requests

    def get_config(self):
        response = self.requests.get(url=self._base_url)
        return response.json()
    
    def get_setting_config(self,key):
        data = self.get_config()
        if isinstance(data,dict):
            conf = data.get(key, DEFAULT_SETTINGS[key])
        else:
            conf = DEFAULT_SETTINGS[key]
        return conf

                                
configAPI = ConfigAPI()