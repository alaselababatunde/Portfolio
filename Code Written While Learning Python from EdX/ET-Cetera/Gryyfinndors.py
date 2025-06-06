students = [
    {"name": "Harry", "house": "gryyfindor"},
    {"name": "Hermione", "house": "gryyfindor"},
    {"name": "Ron", "house": "gryyfindor"},
    {"name": "Draco", "house": "slytherin"},
]

gryyfindors = filter(lambda s: s["house"] == "gryyfindor" , students)

for gryyfindor in sorted(gryyfindors, key= lambda s: s["name"]):
    print(gryyfindor["name"])