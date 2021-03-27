
# from flask import Flask
# from types import CodeType
# from bytecode import Instr, Bytecode
# from flask import request
# import dis
# import logging


# #app = Flask(__name__)



# def foobar(*args):
#     return 200

# @app.route('/', methods=['GET', 'POST'])
# def proxy():
#     args = request.args
#     args = args.to_dict(flat=True)
#     return foobar(**args)


# @app.route('/update_endpoint', methods=["POST"])
# def update():

#     data = request.get_json()

#     app.logger.info(f"Update called with the following params: {data}")

#     data['co_code'] =  data['co_code'].encode('latin1')
#     data['co_lnotab'] = data['co_lnotab'].encode('latin1')

#     func = data['function']

#     #write current version to db

#     for k,v in data.items():
#         if isinstance(v, list):
#             data[k] = tuple(v)

#     globals()[func].__code__ = CodeType(data["co_argcount"],
#                              data["co_kwonlyargcount"],
#                              data["co_posonlyargcount"],
#                              data["co_nlocals"],
#                              data["co_stacksize"],
#                              data["co_flags"],
#                              data["co_code"],
#                              data["co_consts"],
#                              data["co_names"],
#                              data["co_varnames"],
#                              data["co_filename"],
#                              data["co_name"],
#                              data["co_firstlineno"],
#                              data["co_lnotab"],
#                              data["co_freevars"],
#                              data["co_cellvars"],
#                              )

#     return 200





