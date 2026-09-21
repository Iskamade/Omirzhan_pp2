# simple inheritance


class Animal:

    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("Some sound")


class Dog(Animal):

    def bark(self):
        print("Woof!")


d = Dog("Akbas")
d.make_sound()
d.bark()