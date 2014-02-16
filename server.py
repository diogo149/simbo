import os
import json

import flask

import settings
import distributions
from data_handling import *


app = flask.Flask(__name__,
                  static_folder='static',
                  static_url_path='')


### Schema routes


@app.route('/api/schema/<uuid>', methods=['GET'])
def show_schema(uuid): # not necessary, use single page app
    schema = read_schema(uuid)
    return json.dumps(schema)


@app.route('/api/schema/<uuid>', methods=['POST'])
def overwrite_schema(uuid):
    data = flask.request.json
    if not data:
        flask.abort(400) # bad request
    write_schema(uuid, data)
    return "Success"


### Sample routes


@app.route('/api/sample/<uuid>', methods=['GET'])
def sample_experiment(uuid):
    # TODO take in json (for personalization)
    return get_experiment(uuid)


@app.route('/api/sample/<uuid>', methods=['POST'])
def experiment_results(uuid):
    data = flask.request.json
    if (not data
        or "_id" not in data
        or "_obj" not in data):
        flask.abort(400) # bad request
    # TODO handle data
    return "Success"


### Misc routes


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
    app.run()
