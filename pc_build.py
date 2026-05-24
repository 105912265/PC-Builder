import random

class PCBUILD:
    def __init__(self):
        self.components = []

    def add_component(self, components):
        self.components.append(components)

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

    def show_components(self):
        return self.components