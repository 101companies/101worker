def getexcept(code):
    try:
        code()
    except BaseException as e:
        return e
    return None

def dies_ok(code, message=None):
    ok(getexcept(code), message)

def lives_ok(code, message=None):
    ok(getexcept(code) is None, message)
