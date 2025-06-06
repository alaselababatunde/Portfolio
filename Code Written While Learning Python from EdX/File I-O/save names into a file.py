import time

time.sleep(2)

name = input("What's your Name? ")
print(f"Hello, {name}")

with open("names.txt", "a") as file:
    file.write(f"{name}\n")
    
    time.sleep(2)