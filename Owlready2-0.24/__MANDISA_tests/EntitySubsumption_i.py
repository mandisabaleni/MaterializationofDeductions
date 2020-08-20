from owlready2 import *

test_file_path = "/Users/mandisabaleni/Desktop/testsamplemodels"
onto_path.append(test_file_path)
onto = get_ontology("http://www.semanticweb.org/jiba/ontologies/2017/2/test_mixed.owl")


class Parent(Thing):
  namespace = onto
  def test(self): return "ok1"
  def test_inherited(self): return "ok"

class Child(Thing):
  namespace = onto
  def test(self): return "ok2"


  >>> from owlready2 import *
  >>> onto_path.append("/path/to/your/local/ontology/repository")
  >>> onto = get_ontology("http://www.lesfleursdunormal.fr/static/_downloads/pizza_onto.owl")
    >>> onto.load()
