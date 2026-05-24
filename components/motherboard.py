from components.components import Components

class Motherboard(Components):
    def __init__(self, name, brand, price, wattage, socket, ram_type, wifi):
        super().__init__(name, brand, price, wattage)
        self.wattage = wattage
        self.socket = socket
        self.ram_type = ram_type
        self.wifi = wifi
        self.wattage = wattage

    def display_info(self):
        return f"Brand: {self.brand}, Name: {self.name}, Price: {self.price}, Wattage: {self.wattage}, Socket: {self.socket}, RAM_Type: {self.ram_type}, WIFI: {self.wifi}"
    