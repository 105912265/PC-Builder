#Author: Kshitij Kshirsagar
#Filename: cpu.py
#Last edited: 24/05/2026

from components.components import Components

class CPU(Components):
    def __init__(self, name, brand, price, wattage, cores, socket):
        super().__init__(name, brand, price, wattage)
        self.cpu = []
        self.wattage = wattage
        self.cores = cores
        self.socket = socket

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}, Cores: {self.cores}, Socket: {self.socket}"
    


