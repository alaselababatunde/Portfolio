students = [
    {"Name":"Ebenezer", "Class":"100 Level"},
    {"Name":"David", "Class":"SS1 Science"}
]

for index, student in enumerate(students, start=1):
    print(index, student["Name"], student["Class"], sep=", ")