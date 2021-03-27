# from types import CodeType
# import dis


# def wadd(x, y=1):
#     pow_n = 3
#     result = (x + y) ** pow_n
#     return abs(result)


# def fix_function(func, payload):
#     fn_code = func.__code__
#     func.__code__ = CodeType(fn_code.co_argcount,
#                              fn_code.co_kwonlyargcount,
#                              fn_code.co_posonlyargcount,
#                              fn_code.co_nlocals,
#                              fn_code.co_stacksize,
#                              fn_code.co_flags,
#                              payload,
#                              fn_code.co_consts,
#                              fn_code.co_names,
#                              fn_code.co_varnames,
#                              fn_code.co_filename,
#                              fn_code.co_name,
#                              fn_code.co_firstlineno,
#                              fn_code.co_lnotab,
#                              fn_code.co_freevars,
#                              fn_code.co_cellvars,
#                              )

# payload = wadd.__code__.co_code
# #dis.dis(payload)

# # replace BINARY_ADD (0x17) at position #12 with BINARY_SUBTRACT (0x18)
# subtract_opcode = dis.opmap['BINARY_SUBTRACT'].to_bytes(1, byteorder='little')
# payload = payload[0:8] + subtract_opcode + payload[9:]

# print(wadd(3, 1))  # The result is: 64
# # Now it's (x - y) instead of (x+y)
# fix_function(wadd, payload)
# print(wadd(3, 1))  # The result is: 8