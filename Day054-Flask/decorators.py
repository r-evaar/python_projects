from time import time as tic

def timelapse_decorator(func):
    def wrapper(*args, **kw):
        t = tic()
        results = func(*args, **kw)
        t = tic() - t
        txt = f"### Timelapse for @{func.__name__}: {t:.5f}s ###"
        border = '#'*len(txt)
        print(f"\n{border}\n{txt}\n{border}")
        return results
    return wrapper

@timelapse_decorator
def foo():
    print(sum([i**2 for i in range(int(1e7))]))


if __name__ == '__main__':
    foo()
