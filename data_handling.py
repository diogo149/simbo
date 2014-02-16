from uuid import uuid1
import random
import sys
import time

import joblib

import settings
from distributions import generate_random


def uuid():
    return str(uuid1())


def schema_pkl(uuid):
    return os.join(settings.data_folder,
                   "{}_schema.pkl".format(uuid))


def experiments_pkl(uuid):
    return os.join(settings.data_folder,
                   "{}_experiments.pkl".format(uuid))


def ids_pkl():
    # FIXME move to mongo/any document store asap,
    # this is really bad
    return os.join(settings.data_folder, "ids.pkl")


def read_schema(uuid):
    try:
        schema = joblib.load(schema_pkl(uuid))
    except:
        schema = {}
    return schema


def write_schema(uuid, schema):
    joblib.dump(schema, schema_pkl(uuid))


def read_experiments(uuid):
    try:
        experiments = joblib.load(experiments_pkl(uuid))
    except:
        # if no pre-computed experiments are available,
        # return empty experiment
        experiments = [{}]
    return experiments


def write_experiments(uuid, schema):
    joblib.dump(schema, experiments_pkl(uuid))


def store_experiment(experiment):
    ids = joblib.load(ids_pkl())
    ids[experiment["_id"]] = experiment
    joblib.dump(ids_pkl())


def postprocess_experiment(schema, experiment):
    # making sure that every field in schema is
    # part of the current experiment
    for k, v in schema.items():
        if k not in experiment:
            distribution_type = v["distribution"]
            params = v["params"]
            experiment[k] = generate_random(
                distribution_type,
                params,
                1
            )[0]

    # adding the _id
    experiment["_id"] = uuid()

    # storing the experiment
    store_experiment(experiment)

    return experiment


def get_experiment(uuid):
    schema = read_schema(uuid)
    experiments = read_experiments(uuid)
    experiment = random.sample(experiments, 1)[0]
    experiment = postprocess_experiment(schema, experiment)
    return experiment


def update_dataset(uuid, _id, _obj):
    # TODO
    # read in dataset
    # read in experiment
    # append experiment to dataset
    # read in schema
    # remove cols not in schema
    pass


def sample_points(schema, num):
    pass # TODO


def regenerate_points_loop():
    TQ = TimestampQueue(settings.queue_folder, settings.queue_limit)
    while True:
        val = TQ.pop()
        if val is not None:
            # TODO regenerate points
            pass
        else:
            time.sleep(settings.loop_sleep)


if __name__ == "__main__":
    regenerate_points_loop()
