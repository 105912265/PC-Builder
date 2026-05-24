import random

class PCBUILD:
    def __init__(self):
        self.components = []

    def add_component(self, components):
        self.components.append(components)

    def choose_random_component(self, component_list):
        index = random.randrange(len(component_list))
        self.add_component(component_list[index])

    def total_price(self):
        return sum(component.price for component in self.components)

    def display_build(self):
        for component in self.components:
            print(component.display_info())

    def show_components(self):
        return self.components