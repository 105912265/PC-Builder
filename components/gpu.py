#Author: Kshitij Kshirsagar
#Filename: gpu.py
#Last edited: 24/05/2026

from components.components import Components

class GPU(Components):
    def __init__(self, name, brand, price, wattage, vram):
        super().__init__(name, brand, price, wattage)
        self.wattage = wattage
        self.vram = vram

    def display_info(self):
        #return super().display_info() #runs display_info function off parent
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}, VRAM: {self.vram}"
    