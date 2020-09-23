from owlready2 import *
from owlready2.wrapper import Wrapper
from owlready2.materialize import Materialize
from owlready2.preprocess import Preprocess

test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
input_owl_name = "wrapper_removesubclass"
deductions_owl_name = "temp.owl"
output_owl_name = "EntitySubsumption_o.owl"

onto_path.append(test_file_path)
onto = get_ontology(input_owl_name)
onto.load()

test_onto =get_ontology(deductions_owl_name)
with test_onto:
    sync_reasoner()
print("after reasoning")
test_onto.save()

prep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name, test_file_path + "/" + output_owl_name )
prep.items_original_file()
#prep.find_items()
#material = Materialize(prep.deductions, test_file_path + "/" + input_owl_name, test_file_path + "/" + output_owl_name)
#material.load_input_file()
#material.materialize_deductions()
#material.write_to_RDFXML()

#wrap = Wrapper(material)
#wrap.manage()

