# args and kwargs


def sum_numbers(*args):
    s = 0
    for num in args:
        s += num
    return s


def print_info(**kwargs):
    for key, val in kwargs.items():
        print(key, "=", val)


print(sum_numbers(1, 2, 3, 4))
print_info(name="Ilya", age=22)