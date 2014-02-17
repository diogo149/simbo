import json
import random
from uuid import uuid1
from collections import defaultdict

import requests


schema_url = "http://localhost:5000/api/schema/"
experiment_url = "http://localhost:5000/api/sample/"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
binary_schema = {
    "default": 0,
    "distribution": "binary",
    "params": {}
}

def uuid():
    return str(uuid1())


def gen_schema(keys):
    return {key: binary_schema for key in keys}


def to_int(v):
    try:
        return int(v)
    except:
        return 0

def objective_function(a1, a2, a3, **kwargs):
    return (sum([to_int(x) for x in kwargs.values()])
            + 100 * a1
            + 200 * a2)

keys = ['a' + str(x) for x in range(1, 51)]
experiment = "binary_high" # uuid()
experiment_url += experiment
schema_url += experiment
schema = gen_schema(keys)

requests.post(schema_url, data=json.dumps(schema), headers=headers)

iteration = 0
while True:
    iteration += 1
    print iteration
    r = requests.get(experiment_url)
    in_data = r.json()
    out_data = dict(_id = in_data["_id"], _obj=objective_function(**in_data))
    print out_data
    r = requests.post(experiment_url, data=json.dumps(out_data), headers=headers)
