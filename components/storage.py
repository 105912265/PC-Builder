#Author: Kshitij Kshirsagar
#Filename: storage.py
#Last edited: 24/05/2026

from components.components import Components

class Storage(Components):
    def __init__(self, name, brand, price, wattage, type, capacity):
        super().__init__(name, brand, price, wattage)
        self.wattage = wattage
        self.type = type
        self.capacity = capacity

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}, Type: {self.type}, Capacity: {self.capacity}"
    
