
from flask import Flask

from types import CodeType

from bytecode import Instr, Bytecode
from flask import request

import dis



app = Flask(__name__)


def wadd(x, y):

    pow_n = 3
    result = (x + y) ** pow_n
    return abs(result)

@app.route('/', methods=['GET'])
def proxy():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    return str(wadd(x,y))

@app.route('/update_endpoint', methods=["POST"])
def update():

    #payload = request.data
    params = request.get_json()
    payload = params.get("payload").encode("utf-8")
    func = params.get("func")

    #func = "wadd"

    #payload = unicode_string.encode('utf-8')
    fn_code = globals()[func].__code__

    globals()[func].__code__ = CodeType(fn_code.co_argcount,
                             fn_code.co_kwonlyargcount,
                             fn_code.co_posonlyargcount,
                             fn_code.co_nlocals,
                             fn_code.co_stacksize,
                             fn_code.co_flags,
                             payload,
                             fn_code.co_consts,
                             fn_code.co_names,
                             fn_code.co_varnames,
                             fn_code.co_filename,
                             fn_code.co_name,
                             fn_code.co_firstlineno,
                             fn_code.co_lnotab,
                             fn_code.co_freevars,
                             fn_code.co_cellvars,
                             )

    return "True"



