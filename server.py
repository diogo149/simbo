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
    write_schema(str(uuid), data)
    return "Success"

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


### Misc routes


@app.route('/foobar', methods=['GET'])
def sample_chart():
    return graphs.pie_chart(["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"],
                            [3, 4, 0, 1, 5, 7, 3])


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
