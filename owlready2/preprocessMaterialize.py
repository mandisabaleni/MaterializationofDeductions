from owlready2.deduction import Deduction
from owlready2.namespace import _open_onto_file
from array import array


class PreprocessMaterialize:
    def __init__(self, input_file, deductions_file, output_file):
        self.input_file = input_file
        self.deductions_file = deductions_file
        self.output_file = output_file
        base_iri = '''<?xml version="1.0"?>'''
        self.deduction_object_file = _open_onto_file(base_iri, self.deductions_file, mode="rt", only_local=False)
        self.deductions = []
    """
    reads past XML header
    """
    def exclude_header(self):
        with self.deduction_object_file as f:
            for line in f:
                line = line.strip()
                if line == '''</owl:Ontology>''':
                    print("Header excluded")
    """
    Finds and stores all items(classes, properties etc) to container, returns that container
    """
    def find_items(self):#change ontology line for header part, finds and stores deductions in array
        with self.deduction_object_file as f:
            start_of_header = False
            end_of_header = False
            start_of_deduction = False
            end_of_deduction = False
            end_tag = "@#$%^&RESET"
            item_to_edit = "@#$%^&RESET"
            whole_deduction = ""
            for i, line in enumerate(f):
                if "Ontology" in line:
                    start_of_header = True
                    if '''/>''' in line:
                        end_of_header = True
                        continue
                if (start_of_header == True) and ('''</owl:Ontology>''' in line):
                    end_of_header = True
                    continue
                if start_of_header and end_of_header:#end of header
                    if "rdf:about=" in line:#start of deduction
                        start_of_deduction = True
                        end_of_deduction = False
                        print("start of deduction -->"+line)
                        end_tag = '''</'''+line.strip().split()[0][1:]+'''>'''
                        item_to_edit = line.strip().split()[1][4:]
                        #print(end_tag+" <====end tag")
                        continue
                    if (start_of_deduction is True) and (end_tag in line):#end of a deduction
                        newded = Deduction(item_to_edit, whole_deduction)
                        self.deductions.append(newded)
                        print(newded.toString())
                        end_tag = "@#$%^&RESET"
                        item_to_edit = "@#$%^&RESET"
                        whole_deduction = ""
                        start_of_deduction= False
                        end_of_deduction = True

                    if start_of_deduction:
                        if end_of_deduction is False:#in betwwen here are the actual edits
                           print("in between<---"+line )
                           whole_deduction += line
                           #print("whole deduction---> "+whole_deduction)
                '''            
                print(line)
                print("start header---end header---start deduction---end deduction")
                print(start_of_header,end_of_header,start_of_deduction,end_of_deduction)
                '''

