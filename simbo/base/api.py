import abc
import json
import flask


class ApiBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_feature(self, feature_name, distribution, **kwargs):
        return

    @abc.abstractmethod
    def remove_feature(self, feature_name, **kwargs):
        return

    @abc.abstractmethod
    def add_input_variable(self, variable_name, distribution, **kwargs):
        return

    @abc.abstractmethod
    def remove_input_variable(self, variable_name, **kwargs):
        return

    @abc.abstractmethod
    def get_candidate(self, variables, **kwargs):
        return

    @abc.abstractmethod
    def save_result(self, candidate_id, result, **kwargs):
        return

    def api_dispatch(self, data):
        method = data["method"]
        if not hasattr(self, method):
            msg = "Method %s not found" % method
            raise msg
        result = getattr(foo, method)(**data)
        return json.dumps(result or {})

    def start_server(self):
        app = flask.Flask(__name__)

        @app.route('/', methods=['POST'])
        def api_call():
            data = flask.request.json
            print("Received: %s" % data)
            try:
                return self.api_dispatch(data)
            except Exception as e:
                msg = str(e)
                print("ERROR: " + msg)
                return msg
        app.run()


if __name__ == "__main__":
    class Foo(ApiBase):
        def add_feature(self, **kwargs):
            return "foooo"

    foo = Foo()
    foo.start_server()
