import requests
import dis


def foobar(x, y):
    x = int(x)
    y = int(y)
    pow_n = 3

    result = (x + y) ** pow_n
    return str(abs(result))


d = {}

for attr in dir(foobar.__code__):
    if attr.startswith('co_'):
        val = foobar.__code__.__getattribute__(attr)
        print(attr, type(val))
        if isinstance(val, bytes):
            val = val.decode('latin1')
        if attr == 'co_filename':
            val = "updater.py"
        d[attr] = val

d['function'] = 'foobar'
requests.post(url='http://127.0.0.1:5000/update_endpoint',
                    json=d,
                    headers={'Content-Type': 'application/json'})

res = requests.get(url='http://127.0.0.1:5000/?x=3&y=1')
print(res.text)