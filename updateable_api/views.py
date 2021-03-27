from flask import Blueprint
from flask import request
from types import CodeType
from updateable_api.updateable_functions import foobar
import dis



update_bp = Blueprint('update', __name__)



@update_bp.route('/', methods=['GET'])
def foobar_proxy():
    args = request.args
    args = args.to_dict(flat=True)
    response = foobar(**args)
    return str(response)


@update_bp.route('/update_endpoint', methods=["POST"])
def update():


    data = request.get_json()

    data['co_code'] =  data['co_code'].encode('latin1')
    data['co_lnotab'] = data['co_lnotab'].encode('latin1')

    func = data['function']



    for k,v in data.items():
        if isinstance(v, list):
            data[k] = tuple(v)


    globals()[func].__code__ = CodeType(data["co_argcount"],
                             data["co_kwonlyargcount"],
                             data["co_posonlyargcount"],
                             data["co_nlocals"],
                             data["co_stacksize"],
                             data["co_flags"],
                             data["co_code"],
                             data["co_consts"],
                             data["co_names"],
                             data["co_varnames"],
                             data["co_filename"],
                             data["co_name"],
                             data["co_firstlineno"],
                             data["co_lnotab"],
                             data["co_freevars"],
                             data["co_cellvars"],
                             )
    return 200
