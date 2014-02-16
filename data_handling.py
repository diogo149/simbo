from uuid import uuid1
import random
import sys
import time

import joblib

import settings
import ml
from distributions import generate_random


def uuid():
    return str(uuid1())


def schema_pkl(uuid):
    return os.join(settings.data_folder,
                   "{}_schema.pkl".format(uuid))


def dataset_pkl(uuid):
    return os.join(settings.data_folder,
                   "{}_dataset.pkl".format(uuid))


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


def read_dataset(uuid):
    try:
        dataset = joblib.load(dataset_pkl(uuid))
    except:
        dataset = []
    return dataset


def write_dataset(uuid, dataset):
    joblib.dump(dataset, dataset_pkl(uuid))


def read_experiments(uuid):
    try:
        experiments = joblib.load(experiments_pkl(uuid))
    except:
        # if no pre-computed experiments are available,
        # return empty experiment
        experiments = [{}]
    return experiments


def write_experiments(uuid, experiments):
    joblib.dump(experiments, experiments_pkl(uuid))


def read_experiment():
    try:
        ids = joblib.load(ids_pkl())
    except:
        ids = {}
    return ids


def write_experiment(ids):
    joblib.dump(ids, ids_pkl())


def store_experiment(experiment):
    ids = read_experiment()
    ids[experiment["_id"]] = experiment
    write_experiment(ids)


def get_experiment(_id):
    return read_experiment()[_id]


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
    dataset = read_dataset(uuid)
    experiment = get_experiment(_id)
    experiment[_obj] = _obj
    dataset.append(experiment)
    write_dataset(uuid, dataset)


def sample_points(schema):
    keys = sorted(schema.keys())
    points = []
    for k in keys:
        v = schema[k]
        points.append(generate_random(v['distribution'],
                                      v['params'],
                                      settings.random_points_for_smbo))
    return np.array(points).T


def point_to_experiment(schema, point):
    keys = sorted(schema.keys())
    return dict(zip(keys, point))


def dataset_to_matrix(schema, dataset):
    keys = sorted(schema.keys())
    defaults = [schema[k]['default'] for k in keys]

    train = []
    target = []
    for point in dataset:
        row = []
        point_has_data = False
        for key, default in zip(keys, defaults):
            if key in point:
                point_has_data = True
                row.append(point[key])
            else:
                row.append(default)

        # ignoring data for old experiments,
        # should probably prune
        if point_has_data:
            row.append()
            target.append(point["_obj"])

    return train, target


def regenerate_points(uuid):
    schema = read_schema(uuid)
    dataset = read_dataset(uuid)
    train, target = dataset_to_matrix(schema, dataset)
    points = sample_points(schema)
    scores, importances = ml.score_points(train, target, points)

    # TODO save feature importances

    # save top points
    top_points = sorted(zip(scores, points))[:settings.keep_points]
    experiments = map(point_to_experiment, top_points)
    write_experiments(uuid, experiments)


def regenerate_points_loop():
    TQ = TimestampQueue(settings.queue_folder, settings.queue_limit)
    while True:
        val = TQ.pop()
        if val is not None:
            regenerate_points(val)
        else:
            time.sleep(settings.loop_sleep)


if __name__ == "__main__":
    regenerate_points_loop()
