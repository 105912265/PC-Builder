
from components.components import Components

class PSU(Components):
    def __init__(self, name, brand, price, watts):
        super().__init__(name, brand, price)
        self.watts = watts

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Watts: {self.watts}"
    
