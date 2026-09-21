# method overriding


class Animal:

    def speak(self):
        print("Animal speaks")


class Cat(Animal):

    def speak(self):
        print("Meow")


c = Cat()
c.speak()