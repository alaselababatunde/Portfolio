students = [
    {"name": "hermione", "house": "gryffindor"},
    {"name": "harry", "house": "gryffindor"},
    {"name": "ron", "house": "gryffindor"},
    {"name": "draco", "house": "slytherin"},
    {"name": "padma", "house": "ravenclaw"},
]

houses = set()
for student in students:
    if student ["house"] not in houses:
        houses.add(student["house"])

for house in sorted(houses):
    print(houses)