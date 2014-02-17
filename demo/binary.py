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


def objective_function(a, b, **kwargs):
    return (0.5
            + random.uniform(0, 1)
            + 3 * a
            + 2 * b
            - 5 * (a * b))

keys = ['a', 'b']
experiment = uuid()
experiment_url += experiment
schema_url += experiment
schema = gen_schema(keys)

requests.post(schema_url, data=json.dumps(schema), headers=headers)

distribution = defaultdict(lambda: 0)

while True:
    r = requests.get(experiment_url)
    in_data = r.json()
    distribution[(in_data["a"], in_data["b"])] += 1
    print in_data
    print distribution
    out_data = dict(_id = in_data["_id"], _obj=objective_function(**in_data))
    print out_data
    r = requests.post(experiment_url, data=json.dumps(out_data), headers=headers)
