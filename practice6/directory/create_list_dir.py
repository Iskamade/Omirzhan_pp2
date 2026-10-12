import os

os.makedirs("Practice6/files/documents", exist_ok=True)
print("Directories created.")
import os

print(os.listdir("."))
import os

for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)