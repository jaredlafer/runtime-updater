from flask import Blueprint, request, jsonify, make_response
from flask import current_app
from types import CodeType
from updateable_api.updateable_functions import foobar
import dis
import json


update_bp = Blueprint('update', __name__)


@update_bp.route('/', methods=['GET'])
def foobar_endpoint():
    """
    Arbitrary endpoint
    """
    args = request.args
    args = args.to_dict(flat=True)
    response = foobar(**args)
    return make_response(jsonify(response), 200)


@update_bp.route('/update_endpoint', methods=["POST"])
def update():

    data = request.get_json()

    #encode bytes
    data['co_code'] = data['co_code'].encode('latin1')
    data['co_lnotab'] = data['co_lnotab'].encode('latin1')

    func = data['function']

    #json serializes tuples to lists, so this inverses that operation
    for k, v in data.items():
        if isinstance(v, list):
            data[k] = tuple(v)

    #func must be in global scope. 
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

    return make_response(jsonify({'Success': 'Updated'}), 200)
