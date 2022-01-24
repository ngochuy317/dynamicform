import json
from bson import json_util, ObjectId


def convert_json(object):
    return json.loads(json_util.dumps(object))
