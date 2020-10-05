from owlready2 import *
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess

test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
input_owl_name = "EntitySubsumptionbinary1-1optional_i"
deductions_owl_name = "temp.owl"
output_owl_name = "EntitySubsumption_o.owl"

onto_path.append(test_file_path)
onto = get_ontology(input_owl_name)
onto.load()
print(list(onto.classes()))
print(list(onto.object_properties()))
print(list(onto.object_properties()))

test_onto =get_ontology(deductions_owl_name)
with test_onto:#change back to test_onto
    sync_reasoner()
print("after reasoning")
test_onto.save()#change back to test_onto

prep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name, test_file_path + "/" + output_owl_name )
prep.find_items()
material = Materialize(prep.deductions, test_file_path + "/" + input_owl_name, test_file_path + "/" + output_owl_name,prep)
#material.load_input_file()
material.materialize_deductions()
material.write_to_RDFXML()
'''
for i in prep.deductions:
    print(i.toString())
'''


