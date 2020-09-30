from owlready2.__MANDISA_tests.deduction import Deduction
from owlready2.__MANDISA_tests.item import Item
from owlready2.namespace import _open_onto_file

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
    reads past XML header
    """
    def exclude_header(self):
        with self.deduction_object_file as f:
            for line in f:
                line = line.strip()
                if line == '''</owl:Ontology>''':
                    print("Header excluded")

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
                        #print(header)
                    return header + "\n\n"
                else: header += line

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

                #if "Ontology" in line:
                 #   start_of_header = True
                  #  if '''/>''' in line:
                   #     end_of_header = True
                    #    continue
                #if (start_of_header == True) and ('''</owl:Ontology>''' in line):
                 #   end_of_header = True
                  #  continue

                if ('''</owl:Ontology>''' in line) or (('''<owl:Ontology''' in line) and ('''/>''' in line)):
                    start_of_header = True
                    end_of_header = True
                if start_of_header and end_of_header:#end of header
                    if "rdf:about=" in line:#start of deduction
                        start_of_deduction = True
                        end_of_deduction = False
                        #print("start of deduction -->"+line)
                        end_tag = '''</'''+line.strip().split()[0][1:]+'''>'''
                        item_to_edit = line.strip().split()[1][4:]
                        #print(end_tag+" <====end tag")
                        continue
                    if (start_of_deduction is True) and (end_tag in line):#end of a deduction
                        newded = Deduction(item_to_edit, whole_deduction)
                        self.deductions.append(newded)
                        #print(newded.toString())
                        end_tag = "@#$%^&RESET"
                        item_to_edit = "@#$%^&RESET"
                        whole_deduction = ""
                        start_of_deduction= False
                        end_of_deduction = True

                    if start_of_deduction:
                        if end_of_deduction is False:#in betwwen here are the actual edits
                           #print("in between<---"+line )
                           whole_deduction += line
                           #print("whole deduction---> "+whole_deduction)
                '''            
                print(line)
                print("start header---end header---start deduction---end deduction")
                print(start_of_header,end_of_header,start_of_deduction,end_of_deduction)
                '''
    def items_original_file(self):
       with _open_onto_file(self.base_iri, self.input_file, mode="rt", only_local=False) as f:
           stack = []
           in_item = False
           eq = False
           temp_str = ''

           for i, line in enumerate(f):
               temp_str += line
               if stack == []: in_item = False
               else: in_item = True

               #print("eq --->" )
               #print(eq)
               #(line)

               if (line.strip()[:1] == "<") :#and (line.strip()[:2] != "</") : #if opening new bracket i.e <
                   stack.append(line)
                   in_item = True
               if("/>" in line)  or (">" in line): #if closing bracket  or ("</" in line)
                   ele = stack.pop()
                   if "<owl:Class rdf:about=" in ele:
                       in_item = False
                       eq = False
                       temp_str = ''
                   else:
                       if "</owl:equivalentClass>" in ele:
                           self.items[-1].eq += temp_str
                           temp_str = ''
                           eq = False
                       if ("</rdfs:subClassOf>" in ele) and (eq==False):#cardinality restriction
                           self.items[-1].card_restr += temp_str
                           temp_str = ''

               if "<owl:Class rdf:about=" in line: #if beginning of new class item
                   #in_item = True
                   index = line.index("rdf:about=")
                   #item_type = line[:index].strip()
                   item_name = line[index+11:line.rindex("\"")].strip()
                   self.items.append(Item(line))#alt to add with item_name
               if "<owl:ObjectProperty rdf:about=" in line:#if beginning of new obj prop item
                   index = line.index("rdf:about=")
                   item_name = line[index + 11:line.rindex("\"")].strip()
                   self.obj_items.append(Item(line))#alt to add with item_name
               if in_item:
                   if "<rdfs:subPropertyOf" in line:
                       self.obj_items[-1].bool_parent = True
                       self.obj_items[-1].parent += line
                   #if domain and range etc.
                   if "<rdfs:domain" in line:
                       self.obj_items[-1].bool_domain = True
                       self.obj_items[-1].domain += line
                   if "<rdfs:range" in line:
                       self.obj_items[-1].bool_range = True
                       self.obj_items[-1].range += line

                   if ("<rdfs:subClassOf" in line) and (line[line.index("<rdfs:subClassOf")+17: ].strip()!='') and (eq==False):#if parent class no empty subclass of
                       self.items[-1].bool_parent = True
                       self.items[-1].parent += line
                   if "<owl:disjointWith" in line:
                       self.items[-1].bool_disjoint = True
                       self.items[-1].disjoint += line
                   if "<owl:equivalentClass>" in line:
                       eq = True
                       self.items[-1].bool_eq = True
                       temp_str = line
                   if ("<rdfs:subClassOf" in line) and (line[line.index("<rdfs:subClassOf") + 17:].strip() == '') and (eq==False):#if subclass for cardinality restriction
                       self.items[-1].bool_card_restr = True
                       temp_str = line
       return self.items #access via object rather




    '''
           #self.items.pop(0)
           for i in self.obj_items:
               print("\n\n\n ------------------------\nName")
               print(i.name)
               print("Parents")
               print(i.parent)
           for i in self.items:
               print("\n\n\n ------------------------\nName")
               print(i.name)
               print("Equivalent classes")
               print(i.eq)
               print("Cardinality restrictions")
               print(i.card_restr)
               print("Parents")
               print(i.parent)
               print("Disjoint")
               print(i.disjoint)
          '''