import requests
import json
from .config import types


def data_request(method=None, headers=dict(), url=None, data=dict(), validated_user=''):
    if headers["user-auth"] == validated_user:
        try:
            response = requests.request(
                method=method, headers=headers, url=url, data=data)
            if response.status_code == 200:
                return json.loads(response.text)
            return {"message": response.status_code}
        except Exception as e:
            return {"message": f'Failed {method} from url: {url} - {e}'}
    return {"message": f'User {headers["user-auth"]} is not authenticated'}


def fetch_api(self, url):
    headers = dict(self.request.headers)
    headers["user-auth"] = str(self.request.user)
    headers["Accept"] = "application/json"

    response = {
        "form": data_request(
            method="GET",
            headers=headers,
            url=url,
            validated_user="AnonymousUser"
        ),
    }
    return response


def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


def structure_serialize(func, format, json_object):
    if format == 'JSON':
        return func(json_object)
    # The rest of the code remains the same
    else:
        raise ValueError(format)


def serialize_to_json(json_object, payload={},):
    data_structure = list(find('name', json_object))
    validation = list(find('validation', json_object))
    type = list(find('type', json_object))
    for i in range(len(type)):
        if type[i] not in types:
            type[i] = "UNKNOW"

    for item, val, type in zip(data_structure, validation, type):
        payload[item] = types[type](**val)
    return payload
