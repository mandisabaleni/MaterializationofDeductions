from owlready2 import *
from owlready2.__MANDISA_tests.materialize import Materialize
from owlready2.__MANDISA_tests.preprocess import Preprocess

test_file_path ="/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
input_owl_name = "EntitySubsumptionbinary1-Nmand_i"
deductions_owl_name = "temp"
output_owl_name = "relationshipsubsumption1-1_o"

onto_path.append(test_file_path)
onto = get_ontology(input_owl_name)
onto.load()
print(list(onto.classes()))
print(list(onto.object_properties()))

test_onto = get_ontology(deductions_owl_name)
with test_onto:#test_onto
    sync_reasoner()
print("after reasoning")
test_onto.save()#test_onto

prep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name, test_file_path + "/" + output_owl_name )
prep.find_items()
material = Materialize(prep.deductions, test_file_path + "/" + input_owl_name, test_file_path + "/" + output_owl_name, prep)
material.load_input_file()
material.materialize_deductions()
material.write_to_RDFXML()

for i in prep.deductions:
    print(i.toString())

