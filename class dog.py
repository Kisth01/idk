class Dog:
    
    def __init__ (self, name, age):
        self.name = name
        self.age = age
        
    def sit(self):
        print(f"{self.name} is now sitting")
    
    def roll_over(self):
        print(f"{self.name} rolled now!")
        
my_dog = Dog('Степа', 3)
my_dog.sit()
my_dog.roll_over()
print(my_dog.name)
print(my_dog.age)

your_dog = Dog('Cara', 5)
your_dog.sit()
your_dog.roll_over()
print(your_dog.name)
print(your_dog.age)