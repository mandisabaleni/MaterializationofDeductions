from owlready2 import *

test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
owl_name = "EntitySubsumption_i.owl"

onto_path.append(test_file_path)
onto = get_ontology(owl_name)
onto.load()
print(list(onto.classes()))
print(list(onto.object_properties()))
"""""

class Parent(Thing):
  namespace = onto
  def test(self): return "ok1"
  def test_inherited(self): return "ok"

class Child(Thing):
  namespace = onto
  def test(self): return "ok2" 
"""

