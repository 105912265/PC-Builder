#Author: Kshitij Kshirsagar
#Filename: ram.py
#Last edited: 06/06/2026

from components.components import Components

class RAM(Components):
    def __init__(self, name,price, wattage, size_gb, ram_type):
        super().__init__(name, price, wattage)
        self.wattage = wattage
        self.size_gb = size_gb
        self.ram_type = ram_type

    def display_info(self):
        return f"Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}, Capacity(GB): {self.size_gb}, Type: {self.ram_type}"
    
