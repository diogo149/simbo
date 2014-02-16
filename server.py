import flask
import json
import joblib

import distributions


app = flask.Flask(__name__,
                  static_folder='static',
                  static_url_path='')

### Utility functions

def schema_pkl(uuid):
    return"data/{}_schema.pkl".format(uuid)


### Schema routes


@app.route('/api/schema/<uuid>', methods=['GET'])
def show_schema(uuid): # not necessary, use single page app
    try:
        schema = joblib.load(schema_pkl(uuid))
    except:
        schema = {}
    return json.dumps(schema)


@app.route('/api/schema/<uuid>', methods=['POST'])
def add_to_schema(uuid):
    data = flask.request.json
    if not data:
        flask.abort(400) # bad request
    joblib.dump(data, schema_pkl(uuid))
    return "Success"


### Sample routes


@app.route('/api/sample/<uuid>', methods=['GET'])
def sample_experiment(uuid):
    # TODO take in json (for personalization)
    # TODO see if any precomputed settings are available
    # TODO fill in missing fields with defaults
    return "TODO"


@app.route('/api/sample/<uuid>', methods=['POST'])
def experiment_results(uuid):
    data = flask.request.json
    if not data:
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
    app.run()
