def file(filename):
    with open(f'./styles/{filename}.css', 'r') as f:
        style_string = f.read()
    return style_string

def style(style_type):

    if style_type == 'default':
        selected_style = file('default')

    def decorator(func):
        def wrapper(*arg, **kw):
            res = func(*arg, **kw)
            styled = f'<style>{selected_style}</style>'
            return styled + res

        return wrapper

    return decorator
