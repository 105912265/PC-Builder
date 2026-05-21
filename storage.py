
from components import Components

class Storage(Components):
    def __init__(self, name, brand, price, type, capacity):
        super().__init__(name, brand, price)
        self.type = type
        self.capacity = capacity

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Type: {self.type}, Capacity: {self.capacity}"
    
