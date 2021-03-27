import requests
import dis

import flask_unittest

class TestUpdate(flask_unittest.AppTestCase):

    def create_app(self):
        from updateable_api import create_app
        app = create_app()
        yield app

    def test_update_function(self, app):
        
        #*********** function to inject ***********
        def foobar(x, y):
            x = int(x)
            y = int(y)
            pow_n = 3

            result = (x - y) ** pow_n
            return abs(result)
        #*********** end function ***********


        #store the function bytecode and properties in a dict to be posted
        bytecode_dict = {}

        for attr in dir(foobar.__code__):
            if attr.startswith('co_'):
                val = foobar.__code__.__getattribute__(attr)
                if isinstance(val, bytes):
                    val = val.decode('latin1')
                if attr == 'co_filename':
                    val = "updateable_functions.py"
                bytecode_dict[attr] = val

        with app.test_client() as client:
            response = client.post('http://127.0.0.1:5000/update_endpoint',
                    json=bytecode_dict,
                    headers={'Content-Type': 'application/json'})

            print(response)

            res = client.get('http://127.0.0.1:5000/?x=3&y=1')
            print(res)




# def foobar(x, y):
#     x = int(x)
#     y = int(y)
#     pow_n = 3

#     result = (x - y) ** pow_n
#     return str(abs(result))


# d = {}

# for attr in dir(foobar.__code__):
#     if attr.startswith('co_'):
#         val = foobar.__code__.__getattribute__(attr)
#         if isinstance(val, bytes):
#             val = val.decode('latin1')
#         if attr == 'co_filename':
#             val = "updateable_functions.py"
#         d[attr] = val

# d['function'] = 'foobar'
# requests.post(url='http://127.0.0.1:5000/update_endpoint',
#                     json=d,
#                     headers={'Content-Type': 'application/json'})

# res = requests.get(url='http://127.0.0.1:5000/?x=3&y=1')
# print(res.text)