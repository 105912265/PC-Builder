
from components import Components

class RAM(Components):
    def __init__(self, name, brand, price, type, frequency):
        super().__init__(name, brand, price)
        self.type = type
        self.frequency = frequency

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Type: {self.type}, Frequency: {self.frequency}"
    
