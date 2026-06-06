#Author: Kshitij Kshirsagar
#Filename: components.py
#Last edited: 24/05/2026

class Components: 
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_info(self):
        return f"Name: {self.name}, Price: {self.price}"
        
