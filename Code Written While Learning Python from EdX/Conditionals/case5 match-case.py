name = input ("what's your name? ")

match name:
    case "Harry" | "Hermione" | "Ron":
        print("Lives in Gryffindor")
    case "Draco":
        print("Lives in Slytherin")
    case _:
        print ("Who? ")