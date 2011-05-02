import sys

# constants
# RS => Return Status
RS_SUCCESS = "SUCCESS"
RS_FAILURE = "FAILURE"

def FUNC_NAME(back=0):
    return sys._getframe(back + 1).f_code.co_name

def pack_result(status, msg=None, data=None):
    result = {"status": status}
    if msg: result["message"] = msg
    if data: result["data"] = data
    return result


