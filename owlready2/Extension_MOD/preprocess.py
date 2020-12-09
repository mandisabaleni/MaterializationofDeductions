from owlready2.Extension_MOD.deduction import Deduction
from owlready2.Extension_MOD.item import Item
from owlready2.namespace import _open_onto_file
'''
Preprocess puts all stand-alone deductions written in temporaary file into deduction objects
'''
class Preprocess:
    def __init__(self, input_file, deductions_file, output_file):
        self.input_file = input_file
        self.deductions_file = deductions_file
        self.output_file = output_file
        self.base_iri = '''<?xml version="1.0"?>'''
        self.input_object_file = _open_onto_file(self.base_iri, self.input_file, mode="rt", only_local=False)
        self.deduction_object_file = _open_onto_file(self.base_iri, self.deductions_file, mode="rt", only_local=False)
        self.deductions = []
        self.items = []
        self.obj_items = []
        self.header = ''
    """
    Exclude_header reads past XML header
    """
    def exclude_header(self):
        with self.deduction_object_file as f:
            for line in f:
                line = line.strip()
                if line == '''</owl:Ontology>''':
                    print("Header excluded")
    '''
    Get_header retrieves header of input file
    '''
    def get_header(self):
        with _open_onto_file(self.base_iri, self.input_file, mode="rt", only_local=False) as f:
            header = ''
            for i, line in enumerate(f):
                '''
                if i == 0:
                    index = line.index('<?xml version="')
                    num = int(line[index+15:line.index('.')])
                    header += '<?xml version="'+str(num+1)+'.0"?>\n'
                else:
                '''
                if ('''</owl:Ontology>''' in line) or (    ('''<owl:Ontology''' in line) and ('''/>'''in line)    ):
                    header += line
                    return header + "\n\n"
                else: header += line

    """
    Find_items finds and stores all items(classes, properties etc) to container, returns that container
    """
    def find_items(self):
        with self.deduction_object_file as f:
            start_of_header = False
            end_of_header = False
            start_of_deduction = False
            end_of_deduction = False
            end_tag = "@#$%^&RESET"
            item_to_edit = "@#$%^&RESET"
            whole_deduction = ""
            for i, line in enumerate(f):
                if end_of_header == False:
                    self.header +=line

                if ('''</owl:Ontology>''' in line) or (('''<owl:Ontology''' in line) and ('''/>''' in line)):
                    start_of_header = True
                    end_of_header = True
                if start_of_header and end_of_header:
                    if "rdf:about=" in line:
                        start_of_deduction = True
                        end_of_deduction = False
                        end_tag = '''</'''+line.strip().split()[0][1:]+'''>'''
                        item_to_edit = line.strip().split()[1][4:]

                        continue
                    if (start_of_deduction is True) and (end_tag in line):
                        newded = Deduction(item_to_edit, whole_deduction)
                        self.deductions.append(newded)
                        end_tag = "@#$%^&RESET"
                        item_to_edit = "@#$%^&RESET"
                        whole_deduction = ""
                        start_of_deduction= False
                        end_of_deduction = True

                    if start_of_deduction:
                        if end_of_deduction is False:
                           whole_deduction += line
