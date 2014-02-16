import flask


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


@app.route('/experiment/sample/<uuid>', methods=['GET'])
def sample_experiment(uuid):
    return "TODO"


@app.route('/experiment/sample/<uuid>', methods=['POST'])
def experiment_results(uuid):
    data = flask.request.json
    print data
    if not data:
        flask.abort(400) # bad request
    # TODO handle data
    return "Success"


if __name__ == '__main__':
    app.run()
