class Employee:
    def __init__(self, *args):
        if len(args) < 4:
            self.id = 1000
            self.firstname = "Unknown"
            self.lastname = "Unknown"
            self.salary = 0
        else:
            self.id = args[0]
            self.firstname = args[1]
            self.lastname = args[2]
            self.salary = args[3]

    def getid(self):
        return self.id

    def getfirstname(self):
        return self.firstname

    def getlastname(self):
        return self.lastname

    def getsalary(self):
        return self.salary

    def setid(self, id):
        self.id = id

    def setfirstname(self, firstname):
        self.firstname = firstname

    def setlastname(self, lastname):
        self.lastname = lastname

    def setsalary(self, salary):
        self.salary = salary

    def display(self):
        print("Employee ID: ", self.id, "\nFirst Name: ", self.firstname, "\nLast Name: ", self.lastname, "\nSalary: ", self.salary)


emp1 = Employee()
emp1.display()
emp2 = Employee(1234, "Bob", "Smith", 100)
print()
emp1.setid(2345)
emp1.setfirstname("Alasela")
emp1.setlastname("Babatunde")
emp1.setsalary(1000000)
emp1.display()
print()
emp2.display()
