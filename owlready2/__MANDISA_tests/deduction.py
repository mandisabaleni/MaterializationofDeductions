from owlready2 import *

class Deduction:
    def __init__(self, item_to_edit, edit):
        self.item_to_edit = item_to_edit
        self.edit = edit
        self.type = type
    def toString(self):
        print("ITEM TO EDIT:")
        print("--------------")
        print(self.item_to_edit)
        print("DEDUCTION TO BE ADDED:")
        print("--------------")
        print(self.edit)