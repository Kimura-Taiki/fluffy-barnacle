class ReturnValue(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

def enable_ret(func):
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReturnValue as exc:
            return exc.value
    return decorated_func

def ret(value):
    raise ReturnValue(value)

@enable_ret
def testfunc(x):
    ret(None) if x is None else 0
    # in a real use-case there would be more code here
    # ...
    print("hey")
    return 1

print(testfunc(None))
print(testfunc(1))
