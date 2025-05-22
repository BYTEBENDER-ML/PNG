class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def detail(self):
        print(f"Car Brand: {self.brand}, Model: {self.model}")

class HybridCar(Car):
    def __init__(self, brand, model, fuel1, fuel2):
        super().__init__(brand, model)
        self.fuel1 = fuel1
        self.fuel2 = fuel2

    def choice(self):
        print(f"Fuel Options: {self.fuel1} and {self.fuel2}")

# Creating an object
my_hybrid = HybridCar("Toyota", "Prius", "Petrol", "Electric")
my_hybrid.detail()
my_hybrid.choice()