 
from components import Components

class GPU(Components):
    def __init__(self, name, brand, price, vram):
        super().__init__(name, brand, price)
        self.vram = vram

    def display_info(self):
        #return super().display_info() #runs display_info function off parent
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, VRAM: {self.vram}"
    