# class variable vs instance variable


class Student:
    school = "High School"  # common variable

    def __init__(self, name):
        self.name = name


s1 = Student("Jhon")
s2 = Student("Ternus")

print(s1.name, s1.school)
print(s2.name, s2.school)