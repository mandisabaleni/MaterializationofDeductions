from owlready2.Extension_MOD.manager import Manager
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.namespace import _open_onto_file
from owlready2 import *
from owlready2.Extension_MOD.wrapper import Wrapper
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess
'''
This is the initial user interface for user interaction to 
attain OWL file name, specifically its full path and an empty output OWL file.
The class calls on the manager to manage materialization of deductions
'''
def main():
    print("\nWELCOME TO THE EXTENDED TOOL FOR OWLREADY\n_________________________________\n")
    print("Please enter a file path for an input OWL file:\n")
    input_file_full_OWL_path = input()
    if '.owl'in input_file_full_OWL_path:
        input_file_full_OWL_path = input_file_full_OWL_path[:input_file_full_OWL_path.rindex(".owl")]

    print("Please enter a file path for an empty output OWL file:\n")
    output_file_full_OWL_path = input()
    output_file_full_OWL_path = output_file_full_OWL_path

    print(input_file_full_OWL_path)
    print(output_file_full_OWL_path)

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
