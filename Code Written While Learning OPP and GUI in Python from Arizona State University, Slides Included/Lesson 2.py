class HospitalEmployee:

    def __init__(self, empName, empNumber, hourlyPay, hoursWorked):
        self.empName = empName
        self.empNumber = empNumber
        self.hourlyPay = hourlyPay
        self.hoursWorked = hoursWorked
        self.pay = 0;

    def setName(self, empName):
        self.empName = empName

    def setNumber(self, empNumber):
        self.empNumber = empNumber

    def setPay(self, hourlyPay):
        self.hourlyPay = hourlyPay

    def setWorked(self, hoursWorked):
        self.hoursWorked = hoursWorked

    def getName(self):
        return self.empName

    def getNumber(self):
        return self.empNumber

    def getPay(self):
        return self.hourlyPay

    def getWorked(self):
        return self.hoursWorked

    def calculatePay(self):
        self.pay = self.hoursWorked * self.hourlyPay

    def display(self):
        self.calculatePay()
        print("Name: ", self.empName, "\nEmployee Number: ", self.empNumber, "\nEmployee Pay Rate: ", self.hourlyPay)
        print("Hours Worked: ", self.hoursWorked, "\nPay: ", "${:,.2f}".format(self.pay))


class Doctor(HospitalEmployee):
    def __init__(self, specialty, empName, empNumber, hourlyPay, hoursWorked):
        self.specialty = specialty
        super().__init__(empName, empNumber, hourlyPay, hoursWorked)

    def display(self):
        super().display()
        print("Specialty: ", self.specialty)


class Nurse(HospitalEmployee):
    def __init__(self, specialty, empName, empNumber, hourlyPay, hoursWorked):
        self.specialty = specialty
        super().__init__(empName, empNumber, hourlyPay, hoursWorked)

    def display(self):
        super().display()
        print("Specialty: ", self.specialty)


emp1 = Nurse("Trama", "Tina Baldwin", 1223212, 65.54, 40)
emp1.display()
print()
emp2 = Doctor("LnD", "Michael Smith", 12345678, 89.54, 40)
emp2.display()
