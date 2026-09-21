# init example


class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = Person("Tim", 20)
print(p1.name, p1.age)