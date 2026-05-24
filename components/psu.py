#Author: Kshitij Kshirsagar
#Filename: psu.py
#Last edited: 24/05/2026

from components.components import Components

class PSU(Components):
    def __init__(self, name, brand, price, wattage):
        super().__init__(name, brand, price, wattage)
        self.wattage = wattage

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Watts: {self.wattage}"
    
