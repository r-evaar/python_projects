
# Accept any number of arguments as a tuple
def print_in_line(*args):
    for n in args:
        print(n)


print_in_line(5, "Hi", 3, {'key': 23659}, 6)

print('-'*30)


def calculate(n, **kwargs):
    print(kwargs)
    print(type(kwargs))

    n += kwargs["add"]
    n *= kwargs["multiply"]
    return n


num = calculate(2, add=3, multiply=5)
print(num)
