class Student:
    def __init__(self, name, home):
        self.name = name
        self.home = home

    def __str__ (self):
        return f"{self.name} is from {self.home}"
     
    @classmethod   
    def get(cls):
        name = input("Name: ")
        home = input("Home Town: ")
        return cls(name, home)
        ...

def main():
    student = Student.get()
    print(student)
    

if __name__ == "__main__":
    main()