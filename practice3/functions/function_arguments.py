# arguments examples


def show_pet(name, pet="dog"):
    print("My", pet, "is named", name)


def my_mult(a, b, /):
    return a * b


show_pet("Akbas")
show_pet("Borya", "cat")

res = my_mult(3, 4)
print(res)