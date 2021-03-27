from flask import Blueprint, request, jsonify, make_response
from types import CodeType
from updateable_api.updateable_functions import foobar
import dis
import json

# version updateable_api by declaring multiple blueprint versions here
update_bp_v1 = Blueprint('update_v1', __name__)


@update_bp_v1.route('/', methods=['GET'])
def foobar_endpoint():
    """
    Arbitrary endpoint
    """
    args = request.args
    args = args.to_dict(flat=True)
    rv = foobar(**args)
    return make_response(jsonify(rv), 200)


@update_bp_v1.route('/update_endpoint', methods=["POST"])
def update():

    data = request.get_json()

    # encode bytes
    data['co_code'] = data['co_code'].encode('latin1')
    data['co_lnotab'] = data['co_lnotab'].encode('latin1')

    target_func = data['function']

    # if no target function/file provided then no update should be performed. otherwise,
    # exceptions caused by the Code Object update will be handled naturally
    assert target_func is not None and target_func != ""

    # json serializes tuples to lists, so this inverses that operation
    for k, v in data.items():
        if isinstance(v, list):
            data[k] = tuple(v)

    # get the first line number of the target function
    first_line_of_function = globals()[target_func].__code__.__getattribute__("co_firstlineno")

    # target_func must be in global scope.
    globals()[target_func].__code__ = CodeType(data["co_argcount"],
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
                                               first_line_of_function,
                                               data["co_lnotab"],
                                               data["co_freevars"],
                                               data["co_cellvars"],
                                               )

    return make_response(jsonify({'Success': 'Updated'}), 200)
