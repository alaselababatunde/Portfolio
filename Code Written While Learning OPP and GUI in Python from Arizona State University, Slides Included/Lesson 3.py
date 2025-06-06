class Vehicle:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def speed(self):
        print("Max speed is: ", self.speed)
    def gears(self):
        print("Max number of gears: ", self.gears)
    def details(self):
        print("Details: ", "\nName: ", self.name ,"\nColor: ",  self.color)

class Car(Vehicle):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.gears = 6
        self.speed = 140

    def speed(self):
        print("Max speed is: ", self.speed)
    def grears(self):
        print("Max number of gears: ", self.gears)
    def details(self):
        super().details()
        print("Gears: ", self.gears ,"\nSpeed: ", self.speed)

class Truck(Vehicle):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.gears = 8
        self.speed = 120

    def speed(self):
        print("Max speed is: " , self.speed)
    def grears(self):
        print("Max number of gears: ", self.gears)
    def details(self):
        super().details()
        print("Gears: ", self.gears ,"\nSpeed: ", self.speed)

car = Car("Corolla", "Blue")
car.details()
print()
truck = Truck("Titian", "Black")
truck.details()
