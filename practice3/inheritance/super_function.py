# using super()


class Person:

    def __init__(self, name):
        self.name = name


class Student(Person):

    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade


st = Student("Tim", 5)
print(st.name, st.grade)