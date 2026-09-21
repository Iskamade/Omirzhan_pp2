# sorted with key

students = [("Alex", 22), ("Tim", 19), ("Cook", 21)]

# sort by age
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)