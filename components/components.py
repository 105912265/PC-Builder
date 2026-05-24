
class Components: 
    def __init__(self, name, brand, price, wattage):
        self.components = []
        self.name = name
        self.brand = brand
        self.price = price
        self.wattage = wattage

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}"
        
