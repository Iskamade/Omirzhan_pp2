f = open("demofile.txt")
print(f.read())
f = open("D:\\myfiles\welcome.txt")
print(f.read())
with open("demofile.txt") as f:
  print(f.read())
f = open("demofile.txt")
print(f.readline())
f.close()
with open("demofile.txt") as f:
  print(f.read(5))
with open("demofile.txt") as f:
  print(f.readline())
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())
with open("demofile.txt") as f:
  for x in f:
    print(x)
with open("test.txt", "w") as file:
    file.write("Hello")
with open("students.txt", "r") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))
print("First student:", lines[0].strip())
with open("notes.txt", "w") as file:
    file.write("First line\n")
    file.write("Second line\n")

    import os
os.remove("demofile.txt")

import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")
import os
os.rmdir("myfolder")