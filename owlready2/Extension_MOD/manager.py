from owlready2 import *
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess

class Manager:
    def __init__(self, test_file_path, input_owl_name, deductions_owl_name, output_owl_name):
        self.test_file_path = test_file_path
        self.input_owl_name = input_owl_name
        self.deductions_owl_name = deductions_owl_name
        self.output_owl_name = output_owl_name

    def manage(self):
        onto_path.append(self.test_file_path)
        onto = get_ontology(self.input_owl_name)
        onto.load()

        test_onto = get_ontology(self.deductions_owl_name)
        with test_onto:
            sync_reasoner()
        print("after reasoning")
        test_onto.save()

        prep = Preprocess(self.test_file_path + "/" + self.input_owl_name, self.test_file_path + "/" + self.deductions_owl_name, self.test_file_path + "/" + self.output_owl_name)
        # prep.items_original_file()

        prep.find_items()
        material = Materialize(prep.deductions, self.test_file_path + "/" + self.input_owl_name, self.test_file_path + "/" + self.output_owl_name, prep)

        material.materialize_deductions()
        material.write_to_RDFXML()
        # print(input_owl_name)
        # print(output_owl_name[:output_owl_name.rindex(".owl")])
        # changedprep.items_original_file(test_file_path + "/" + output_owl_name[:output_owl_name.rindex(".owl")])
        material.items_original_file(self.test_file_path + "/" + self.output_owl_name[:self.output_owl_name.rindex(".owl")])
        items = material.items
        obj_items = material.obj_items
        print("PRINTING ITEMS")
        # for i in items:
        # i.assemble()
        # i.full_item()
        # print(i.full)

        wrap = Wrapper(material, prep)
        wrap.manage()

