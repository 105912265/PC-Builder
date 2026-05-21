
class Components: 
    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}"
        
