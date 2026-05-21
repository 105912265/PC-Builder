
class PCBUILD:
    def __init__(self):
        self.components = []

    def add_component(self, components):
        self.components.append(components)

    def total_price(self):
        return sum(component.price for component in self.components)

    def display_build(self):
        for component in self.components:
            print(component.display_info())