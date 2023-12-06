def success_true_response(message=None, data=None, count=None):
    result = dict(success=True)
    result['message'] = message or ''
    result['data'] = data or {}
    if count is not None:
        result['count'] = count
    return result

def success_false_response(message=None, data=None):
    result = dict(success=False)
    result['message'] = message or ''
    result['data'] = data or {}
    return result