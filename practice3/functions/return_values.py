# return example


def add(a, b):
    return a + b


def get_user():
    name = "Bob"
    age = 20
    return name, age


s = add(5, 10)
print("Sum is:", s)

user_name, user_age = get_user()
print(user_name, user_age)