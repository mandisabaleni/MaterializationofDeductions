from owlready2 import *
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess
'''
Manager is responsible for the core management of materializing deductions in an OWL file
It creates python classes for OWL ontologies and manages the preprocessing class, material class and wrap 
class to make changes to the OWL. Changes come from the resoner.
'''
class Manager:
    def __init__(self, test_file_path, input_owl_name, deductions_owl_name, output_owl_name):
        self.test_file_path = test_file_path
        self.input_owl_name = input_owl_name
        self.deductions_owl_name = deductions_owl_name
        self.output_owl_name = output_owl_name
    '''
    Manage calls all methods in sequence to manage MOD
    '''
    def manage(self):
        onto_path.append(self.test_file_path)
        onto = get_ontology(self.input_owl_name)
        onto.load()

        test_onto = get_ontology(self.deductions_owl_name)
        with test_onto:
            sync_reasoner()
        test_onto.save()

        prep = Preprocess(self.test_file_path + "/" + self.input_owl_name, self.test_file_path + "/" + self.deductions_owl_name, self.test_file_path + "/" + self.output_owl_name)


        prep.find_items()
        material = Materialize(prep.deductions, self.test_file_path + "/" + self.input_owl_name, self.test_file_path + "/" + self.output_owl_name, prep)

        material.materialize_deductions()
        material.write_to_RDFXML()
        material.items_original_file(self.test_file_path + "/" + self.output_owl_name[:self.output_owl_name.rindex(".owl")])

        wrap = Wrapper(material, prep)
        wrap.manage()

