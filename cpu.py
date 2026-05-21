
from components import Components

class CPU(Components):
    def __init__(self, name, brand, price, cores, socket):
        super().__init__(name, brand, price)
        self.cores = cores
        self.socket = socket

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Cores: {self.cores}, Socket: {self.socket}"
    