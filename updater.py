
from flask import Flask
from types import CodeType
from bytecode import Instr, Bytecode
from flask import request
import dis


app = Flask(__name__)

@app.route('/', methods=['GET'])
def foobar(*args):
    return "True"

# @app.route('/', methods=['GET', 'POST'])
# def proxy():
#     args = request.args
#     args = args.to_dict(flat=True)
#     return foobar(**args)


@app.route('/update_endpoint', methods=["POST"])
def update():
    data = request.get_json()

    data['co_code'] =  data['co_code'].encode('latin1')
    data['co_lnotab'] = data['co_lnotab'].encode('latin1')

    func = data['function']

    for k,v in data.items():
        if isinstance(v, list):
            data[k] = tuple(v)

    globals()[func].__code__ = CodeType(data.get("co_argcount"),
                             data.get("co_kwonlyargcount"),
                             data.get("co_posonlyargcount"),
                             data.get("co_nlocals"),
                             data.get("co_stacksize"),
                             data.get("co_flags"),
                             data.get("co_code"),
                             data.get("co_consts"),
                             data.get("co_names"),
                             data.get("co_varnames"),
                             data.get("co_filename"),
                             data.get("co_name"),
                             data.get("co_firstlineno"),
                             data.get("co_lnotab"),
                             data.get("co_freevars"),
                             data.get("co_cellvars"),
                             )

    return "True"





