class Vault:
    def __init__ (self=0, gold=0, silver=0, bronze=0):
        self.gold = gold
        self.silver = silver
        self.bronze = bronze
    
    
    def __str__(self):
        return f"{self.gold} gold, {self.silver} silver, {self.bronze} bronze"
    
    def __add__(self, other):
        gold = self.gold + other.gold
        silver = self.silver + other.silver
        bronze = self.bronze + other.bronze
        return Vault(gold, silver, bronze)
        
        
alasela = Vault(100, 50, 25)
print(alasela)


iremitide = Vault(25, 50, 100)
print(iremitide)


total = alasela + iremitide
print(total)