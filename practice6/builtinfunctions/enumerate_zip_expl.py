names = ["Ali", "Dana", "Arman"]
scores = [90, 85, 95]

for index, name in enumerate(names):
    print(index, name)

for name, score in zip(names, scores):
    print(name, score)
x = "25"

print(type(x))

y = int(x)
z = float(x)

print(y, type(y))
print(z, type(z))
print(str(y), type(str(y)))