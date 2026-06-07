#Author: Kshitij Kshirsagar
#Filename: pc_build.py
#Last edited: 24/05/2026

import random

#consist of all parts needed for pc to function
class PCBUILD:
    def __init__(self):
        self.components = []

    def add_component(self, components):
        self.components.append(components)

    #function to choose random component for random build
    def choose_random_component(self, component_list):
        if not component_list:
            return None
        choice = random.choice(component_list)
        self.add_component(choice)
        return choice

    def total_price(self):
        return sum(component.price for component in self.components)
    
    def total_watts(self):
        return sum(component.wattage for component in self.components)

    def display_build(self):
        for component in self.components:
            print(component.display_info())

    def save_build(self, filename="output/build.txt"):
        with open(filename, "w", encoding="utf8") as file:
            file.write("PC Build Summary\n")
            file.write("----------------\n")

            for component in self.components:
                file.write(component.display_info() + "\n")

            file.write(f"\nTotal price: ${self.total_price()}\n")

    def show_components(self):
        return self.components