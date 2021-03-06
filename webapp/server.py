import os
import json
import distributions
import graphs
from subprocess import Popen

import flask

import settings
import distributions
from data_handling import *
from timestamp_queue import TimestampQueue


TQ = TimestampQueue(settings.queue_folder, settings.queue_limit)

app = flask.Flask(__name__,
                  static_folder='static',
                  static_url_path='')


### Schema routes

@app.route('/api/schema/<string:uuid>', methods=['GET'])
def show_schema(uuid): # not necessary, use single page app
    schema = read_schema(uuid)
    return json.dumps(schema)


@app.route('/api/schema/<string:uuid>', methods=['POST'])
def overwrite_schema(uuid):
    data = flask.request.json
    if not data:
        flask.abort(400) # bad request
    write_schema(uuid, data)
    return json.dumps({})


@app.route('/api/schema/add/<string:uuid>', methods=['POST'])
def add_to_schema(uuid):
    data = flask.request.json
    if not data:
        flask.abort(400) # bad request
    schema = read_schema(uuid)
    schema.update(data)
    write_schema(uuid, schema)
    return json.dumps({})


@app.route('/api/schema/delete/<string:uuid>', methods=['POST'])
def delete_from_schema(uuid):
    data = flask.request.json
    print data
    if not data:
        flask.abort(400) # bad request
    schema = read_schema(uuid)
    for key in data:
        schema.pop(key)
    write_schema(uuid, schema)
    return json.dumps({})


### Sample routes


@app.route('/api/sample/<string:uuid>', methods=['GET'])
def sample_experiment(uuid):
    # future: optionally take in json (for personalization)
    return json.dumps(get_experiment(uuid))


@app.route('/api/sample/<string:uuid>', methods=['POST'])
def experiment_results(uuid):
    data = flask.request.json
    if (not data
        or "_id" not in data
        or "_obj" not in data):
        flask.abort(400) # bad request
    update_dataset(uuid, data["_id"], data["_obj"])
    TQ.push(uuid)
    return "Success"


### Graph routes


@app.route('/api/graph/importances/<string:uuid>', methods=['GET'])
def importances_graph(uuid):
    k, v = load_importances(uuid)
    return graphs.pie_chart(k, v)


@app.route('/api/graph/results/<string:uuid>', methods=['GET'])
def results_graph(uuid):
    xs, ys, keys = results_per_variable(uuid)
    return graphs.scatter_chart(xs, ys, keys)


### Misc routes


@app.route('/test/pie', methods=['GET'])
def sample_pie():
    return graphs.pie_chart(["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"],
                            [3, 4, 0, 1, 5, 7, 3])


@app.route('/test/scatter')
def sample_scatter():
    return graphs.scatter_chart(((1,2,3,4,5),), ((5,4,3,2,1), ), ("test", ))


@app.route('/', methods=['GET'])
def homepage():
    return flask.redirect(flask.url_for('static',
                                        filename='index.html'))


@app.route('/api/distribution_schema')
def distribution_schema():
    return json.dumps(distributions.DISTRIBUTIONS_SCHEMA)


if __name__ == '__main__':
    try:
        os.mkdir(settings.data_folder)
    except OSError:
        pass
    # run background task that takes things off the queue
    # and recomputes samples for experiments
    Popen(["python", "data_handling.py"])
    app.run()
