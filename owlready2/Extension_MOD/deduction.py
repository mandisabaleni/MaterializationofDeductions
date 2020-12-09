from owlready2 import *
'''
This class encapsulates an inference as an object 
edit~the inference to be added to the ontology
item_to_edit ~ the OWL object in the ontology that needs to be edited
'''
class Deduction:
    def __init__(self, item_to_edit, edit):
        self.item_to_edit = item_to_edit
        self.edit = edit
        self.type = type
    '''Prints the deduction object to screen'''
    def toString(self):
        print("ITEM TO EDIT:")
        print("--------------")
        print(self.item_to_edit)
        print("DEDUCTION TO BE ADDED:")
        print("--------------")
        print(self.edit)