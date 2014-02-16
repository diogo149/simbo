import flask
import json
import distributions
import graphs

app = flask.Flask(__name__,
                  static_folder='static',
                  static_url_path='')


@app.route('/', methods=['GET'])
def homepage():
    return flask.redirect(flask.url_for('static',
                                        filename='index.html'))

@app.route('/experiment/<uuid>', methods=['GET'])
def show_experiment(uuid): # not necessary, use single page app
    return "TODO"

@app.route('/foobar', methods=['GET'])
def sample_chart():
    return graphs.pie_chart(["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"],
                            [3, 4, 0, 1, 5, 7, 3])

@app.route('/experiment/sample/<uuid>', methods=['GET'])
def sample_experiment(uuid):
    # TODO take in json (for personalization)
    # TODO see if any precomputed settings are available
    # TODO fill in missing fields with defaults
    return "TODO"


@app.route('/experiment/sample/<uuid>', methods=['POST'])
def experiment_results(uuid):
    data = flask.request.json
    print data
    if not data:
        flask.abort(400) # bad request
    # TODO handle data
    return "Success"


@app.route('/api/distribution_schema')
def distribution_schema():
    return json.dumps(distributions.DISTRIBUTIONS_SCHEMA)


if __name__ == '__main__':
    app.run()
