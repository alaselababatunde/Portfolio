class Wizard:
    def __init__(self, name):
        if not name:
            raise ValueError("Missing name")
        self.name = name
        
    ...


class Student(Wizard):
    def __init__(self, name, house):
        super().__init__(name)
        self.house = house
        
    ...
    
class Professor(Wizard):
    def __init__(self, name, ):
        super().__init__(name)
        self.subject = subject
        
    ...


wizard = Wizard("Albus")
student = Student ("Alasela", "lagos")
professor = Professor ("Bolaji")