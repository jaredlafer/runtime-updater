import requests
import dis
import flask_unittest


class TestUpdate(flask_unittest.AppTestCase):
    """TestUpdate is meant to emulate what would happen on the client side. It creates a function foobar, 
    converts it to CodeObject, and injects that into a function on the server which is also 
    named 'foobar,' though it doesn't have to have the same name. This provides a specification
    for serializing a function on the client and calling the update_function endpoint 
    on the server.
    """

    def create_app(self):
        from updateable_api import create_app
        app = create_app()
        yield app

    def prepare_function(self, func, target_func):
        """
        Prepares a dict containing the attributes of func required for generating a CodeObject 
        and injecting that CodeObject into target_func

        :param func: function object
        :param target_func: name of the target function
        :returns: dict ready to be serialized
        """

        bytecode_dict = {}

        for attr in dir(func.__code__):
            if attr.startswith('co_'):
                val = func.__code__.__getattribute__(attr)
                if isinstance(val, bytes):
                    val = val.decode('latin1')
                if attr == 'co_filename':
                    val = "updateable_functions.py"
                bytecode_dict[attr] = val

        bytecode_dict['function'] = target_func

        return bytecode_dict

    def test_update_function_math(self, app):
        """
        Creates a function that does a mathematical computation and injects it onto the running server

        :param app: Flask app
        """

        # function to inject
        def foobar(x, y):
            x = int(x)
            y = int(y)
            pow_n = 3

            result = (x - y) ** pow_n
            return abs(result)

        bytecode_dict = self.prepare_function(foobar, "foobar")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?x=3&y=1')
            self.assertEqual(8, response.json)

    def test_update_function_string(self, app):
        """
        Creates a function that returns a string and injects it onto the running server

        :param app: Flask app
        """

        # function to inject
        def foobar():
            return "foobar"

        bytecode_dict = self.prepare_function(foobar, "foobar")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?')
            self.assertEqual("foobar", response.json)
