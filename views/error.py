def error_response(msg, code):
    resp = {}
    resp['error_message'] = msg
    resp['status_code'] = code

    return resp

