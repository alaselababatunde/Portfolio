import csv
import time


time.sleep(2)
name = input("What's your Name? ")
home = input("Where's your Home? ")

with open("save students name and home.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name","home"])
    writer.writerow({"name": name, "home": home})
    
    time.sleep(2)