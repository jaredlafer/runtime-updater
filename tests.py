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

    def prepare_function(self, func, target_funcname, target_filename):
        """
        Prepares a dict containing the attributes of func required for generating a CodeObject 
        and injecting that CodeObject into the target function in the target file

        :param func: function object
        :param target_funcname: name of the target function
        :param target_filename: name of the target file
        :returns: dict ready to be serialized
        """

        bytecode_dict = {}

        for attr in dir(func.__code__):
            if attr.startswith('co_'):
                val = func.__code__.__getattribute__(attr)
                #convert bytes to string
                if isinstance(val, bytes):
                    #bytes don't like some other standard encodings
                    val = val.decode('latin1')
                #specify filename
                if attr == 'co_filename':
                    val = target_filename
                bytecode_dict[attr] = val

        bytecode_dict['function'] = target_funcname

        return bytecode_dict

    def test_update_function_math(self, app):
        """
        Creates a function that does a mathematical computation and injects it onto the running server
        """

        # function to inject
        def foobar(x, y):
            x = int(x)
            y = int(y)
            pow_n = 3

            result = (x - y) ** pow_n
            return abs(result)

        bytecode_dict = self.prepare_function(foobar, "foobar", "updateable_functions.py")

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
        """

        # function to inject
        def foobar():
            return "foobar"

        bytecode_dict = self.prepare_function(foobar, "foobar", "updateable_functions.py")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?')
            self.assertEqual("foobar", response.json)


    def test_update_function_two_return_types(self, app):
        """
        Creates a function that returns two objects of different types
        and injects it onto the running server
        """

        # function to inject
        def foobar():
            return "foobar", 5

        bytecode_dict = self.prepare_function(foobar, "foobar", "updateable_functions.py")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?')
            a,b = response.json
            self.assertEqual("foobar", a)
            self.assertEqual(5, b)

    def test_update_function_buggy(self, app):
        """
        Creates a buggy function and injects it onto the running server. Tests
        that a 500 status is returned
        """

        # function to inject
        def foobar():
            raise Exception

        bytecode_dict = self.prepare_function(foobar, "foobar", "updateable_functions.py")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?')
            self.assertEqual(response.status, "500 INTERNAL SERVER ERROR")

    def test_update_function_that_calls_function(self, app):
        """
        Creates a function foobar that calls another function named function_for_foobar_to_call, 
        which also lives on the server
        """

        #since function_for_foobar_to_call() isn't in scope here, need to access through injected globals()
        def foobar():
            return globals()['function_for_foobar_to_call']()

        bytecode_dict = self.prepare_function(foobar, "foobar", "updateable_functions.py")

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                                   json=bytecode_dict,
                                   headers={'Content-Type': 'application/json'})
            self.assertEqual(response.json['Success'], 'Updated')

            response = client.get('http://127.0.0.1:5000/?')
            self.assertEqual(response.json, 1)




    

