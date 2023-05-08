from utils import css
def style(filename):
    def decorator(fun):

        def wrapper(*args, **kw):
            body = fun(*args, **kw)
            return css(filename)+body

        return wrapper

    return decorator
