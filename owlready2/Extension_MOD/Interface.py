from owlready2.Extension_MOD.manager import Manager
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.namespace import _open_onto_file
from owlready2 import *
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess

#/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels/EntitySubsumptionbinary1-1mand_i.owl

def main():
    print("\nWELCOME TO THE EXTENDED TOOL FOR OWLREADY\n_________________________________\n")
    print("Please enter a file path for an input OWL file:\n")
    input_file_full_OWL_path = input()
    if '.owl'in input_file_full_OWL_path:
        input_file_full_OWL_path = input_file_full_OWL_path[:input_file_full_OWL_path.rindex(".owl")]
    '''
    base_iri =''
    f = open(input_file_full_OWL_path, "rb")
    for i in f:
        x = f.readline().decode('ascii')
        if ("RDF xmlns=" in x) or ("xml:base" in x):
            base_iri = x[x.find("\"") + 1:x.rfind("\"")]
    '''
    print("Please enter a file path for an empty output OWL file:\n")
    output_file_full_OWL_path = input()
    output_file_full_OWL_path = output_file_full_OWL_path

    print(input_file_full_OWL_path)
    print(output_file_full_OWL_path)
#/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels/wrapper_removesubclass
#/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels/EntitySubsumption_o.owl

    test_file_path = input_file_full_OWL_path[:input_file_full_OWL_path.rindex("/")]
    input_owl_name = input_file_full_OWL_path[input_file_full_OWL_path.rindex("/")+1:]
    deductions_owl_name = "temp.owl"
    output_owl_name = output_file_full_OWL_path[output_file_full_OWL_path.rindex("/")+1:]

    print(input_owl_name)
    print(output_owl_name)


    manager = Manager(test_file_path,input_owl_name, deductions_owl_name, output_owl_name)
    manager.manage()



if __name__ == "__main__":
    main()
