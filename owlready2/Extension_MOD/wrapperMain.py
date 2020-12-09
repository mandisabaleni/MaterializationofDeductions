from owlready2 import *
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess
'''
DUMMY class used to explore wrapper functionality
'''
test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
input_owl_name = "wrapper_removesubclass"
deductions_owl_name = "temp.owl"
output_owl_name = "remove.owl"
'''
onto_path.append(test_file_path)
onto = get_ontology(input_owl_name)
onto.load()

test_onto =get_ontology(deductions_owl_name)
with test_onto:
    sync_reasoner()
print("after reasoning")
test_onto.save()

prep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name, test_file_path + "/" + output_owl_name )
#prep.items_original_file()

prep.find_items()
material = Materialize(prep.deductions, test_file_path + "/" + input_owl_name, test_file_path + "/" + output_owl_name, prep)

material.materialize_deductions()
material.write_to_RDFXML()
#print(input_owl_name)
#print(output_owl_name[:output_owl_name.rindex(".owl")])
#changedprep.items_original_file(test_file_path + "/" + output_owl_name[:output_owl_name.rindex(".owl")])
material.items_original_file(test_file_path + "/" + output_owl_name[:output_owl_name.rindex(".owl")])
items = material.items
obj_items = material.obj_items
print("PRINTING ITEMS")
#for i in items:
    #i.assemble()
    #i.full_item()
    #print(i.full)

wrap = Wrapper(material, prep)
wrap.manage()
'''
