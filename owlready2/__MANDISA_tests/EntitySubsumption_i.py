from owlready2 import *
from owlready2.preprocessMaterialize import PreprocessMaterialize

test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
owl_name = "EntitySubsumption_i.owl"
owl_name_output_test = "EntitySubsumption_o2.owl"

onto_path.append(test_file_path)
onto = get_ontology(owl_name)
onto.load()
print(list(onto.classes()))
print(list(onto.object_properties()))
print(list(onto.object_properties()))

test_onto =get_ontology(owl_name_output_test)
with test_onto:
    sync_reasoner()
print("after reasoning")
test_onto.save()
prep = PreprocessMaterialize(test_file_path+"/EntitySubsumption_i.owl",test_file_path+"/EntitySubsumption_o2.owl",test_file_path+"/EntitySubsumption_o.owl" )

prep.find_items()
#test_onto.save(file= (test_file_path + "/EntitySubsumption_o2.owl"), format="rdfxml")
"""onto.get_children_of()
"""

