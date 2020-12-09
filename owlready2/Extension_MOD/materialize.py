from owlready2.Extension_MOD.item import Item
from owlready2.namespace import _open_onto_file
'''
Materialize is responsible for editing the ontology with inferences and writing subsequent ontology to file
'''
class Materialize:
    def __init__(self, deductions, input_file, output_file, prep):
        self.preprocess = prep
        self.deductions = deductions
        self.input_file = input_file
        self.output_file = output_file
        self.base_iri =  '''<?xml version="1.0"?>'''
        self.list_file = []
        self.dict_deduction_line = {}
        self.input_object_file = _open_onto_file(self.base_iri, self.input_file, mode="rb", only_local=False)
        self.output_object_file = _open_onto_file(self.base_iri, self.output_file, mode="rb+", only_local=False)
        self.items = []
        self.obj_items = []
        self.header = ''

        self.OBJ_PROP_HEADER = '\n    <!--\n    ///////////////////////////////////////////////////////////////////////////////////////\n    //\n    // Object Properties\n    //\n    ///////////////////////////////////////////////////////////////////////////////////////\n     -->\n\n\n'
        self.CLASS_HEADER = '\n    <!--\n    ///////////////////////////////////////////////////////////////////////////////////////\n    //\n    // Classes\n    //\n    ///////////////////////////////////////////////////////////////////////////////////////\n     -->\n\n\n'
    '''
    Load_input_file loads input file into list for dynamic manioulation
    '''
    def load_input_file(self):
        end_of_header = False
        for line in self.input_object_file:
            self.list_file.append(line)

            if end_of_header == False:
                self.header += line.decode('ascii')
            if ('''</owl:Ontology>'''.encode('ascii') in line) or (('''<owl:Ontology'''.encode('ascii') in line) and ('''/>'''.encode('ascii') in line)):
                self.header += '\n\n'
                end_of_header = True
    '''
    Items_original_file writes the file that has had materialization of deductions performed to Item objects (class and object properties)
    Identifies constraints and stores them accordingly for each class/object property
    input ~ the materialized OWL file
    '''
    def items_original_file(self, input):
        self.items.clear()
        self.obj_items.clear()
        with _open_onto_file(self.base_iri, self.output_file, mode="rt", only_local=False) as f:
            stack = []
            in_item = False
            eq = False
            temp_str = ''
            for i, line in enumerate(f):

                temp_str += line
                if stack == []:
                    in_item = False
                else:
                    in_item = True


                if (line.strip()[:1] == "<"):
                    stack.append(line)
                    in_item = True
                if ("/>" in line) or (">" in line):  # if closing bracket  or ("</" in line)
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
                        if ("</rdfs:subClassOf>" in ele) and (eq == False):  # cardinality restriction
                            self.items[-1].card_restr += temp_str
                            temp_str = ''

                if "<owl:Class rdf:about=" in line:  # if beginning of new class item
                    # in_item = True
                    index = line.index("rdf:about=")
                    # item_type = line[:index].strip()
                    item_name = line[index + 11:line.rindex("\"")].strip()
                    self.items.append(Item(line))  # alt to add with item_name
                if "<owl:ObjectProperty rdf:about=" in line:  # if beginning of new obj prop item
                    index = line.index("rdf:about=")
                    item_name = line[index + 11:line.rindex("\"")].strip()
                    self.obj_items.append(Item(line))  # alt to add with item_name
                if in_item:
                    if "<rdfs:subPropertyOf" in line:
                        self.obj_items[-1].bool_parent = True
                        self.obj_items[-1].parent += line
                    # if domain and range etc.
                    if "<rdfs:domain" in line:
                        self.obj_items[-1].bool_domain = True
                        self.obj_items[-1].domain += line
                    if "<rdfs:range" in line:
                        self.obj_items[-1].bool_range = True
                        self.obj_items[-1].range += line

                    if ("<rdfs:subClassOf" in line) and (line[line.index("<rdfs:subClassOf") + 17:].strip() != '') and (
                            eq == False):  # if parent class no empty subclass of
                        self.items[-1].bool_parent = True
                        self.items[-1].parent += line
                    if "<owl:disjointWith" in line:
                        self.items[-1].bool_disjoint = True
                        self.items[-1].disjoint += line
                    if "<owl:equivalentClass>" in line:
                        eq = True
                        self.items[-1].bool_eq = True
                        temp_str = line
                    if ("<rdfs:subClassOf" in line) and (line[line.index("<rdfs:subClassOf") + 17:].strip() == '') and (
                            eq == False):  # if subclass for cardinality restriction
                        self.items[-1].bool_card_restr = True
                        temp_str = line
    '''
    Materialize_deductions identifies the type of inference to call on relevant function to make appropriate edit
    '''
    def materialize_deductions(self):
        self.load_input_file()
        for i, line in enumerate(self.list_file):
            for deduction in self.deductions:
                index = deduction.item_to_edit.rfind('#')
                refact_item_to_edit = deduction.item_to_edit[:7]+deduction.item_to_edit[index:]

                if ("subClassOf" in deduction.edit) or ("equivalentClass" in deduction.edit):#entity subsumption
                    self.add(i, deduction.item_to_edit.encode('utf_8'), refact_item_to_edit.encode('utf_8'), deduction.edit.encode('utf_8'), line)
                if ("owl#Nothing" in deduction.edit) and ("Class" in deduction.edit):
                    print("inconsistent class")
                    self.add(i, deduction.item_to_edit.encode('utf_8'), refact_item_to_edit.encode('utf_8'), "<!--DEDUCTION-->\n<!--INCONSISTENT CLASS-->\n".encode('utf_8'), line)
    '''
    Write_to_RDFXML writes ontology from dynamic list to OWL file
    '''
    def write_to_RDFXML(self):
        for line in self.list_file:
            self.output_object_file.write(line)
    '''
    Write_to_RDFXML_via_items writes ontology from Item objects list to OWL file
    all_class_items~ classes to be written to file
    all_obj_items~ object properties to be written to file
    '''
    def write_to_RDFXML_via_items(self, all_class_items, all_obj_items):
        with _open_onto_file(self.base_iri, self.output_file, mode="wb", only_local=False) as f:
            f.write(self.preprocess.get_header().encode('ascii'))
            f.write(self.OBJ_PROP_HEADER.encode('ascii'))
            if all_obj_items:
                for o_i in all_obj_items:
                    index = o_i.name.index("rdf:about=")
                    link = o_i.name[index + 11:o_i.name.rindex("\"")].strip()

                    f.write(('\n\n    <!-- '+link+' -->\n\n').encode('ascii'))
                    f.write(o_i.full.encode('ascii'))

            f.write(self.CLASS_HEADER.encode('ascii'))
            if all_class_items:
                for c_i in all_class_items:
                    index = c_i.name.index("rdf:about=")
                    link = c_i.name[index + 11:c_i.name.rindex("\"")].strip()

                    f.write(('\n\n    <!-- ' + link + ' -->\n\n').encode('ascii'))
                    f.write(c_i.full.encode('ascii'))
            f.write('\n</rdf:RDF>'.encode('ascii'))
    '''
    DeleteContent clears output file
    '''
    def deleteContent(self):
        self.output_object_file.seek(0)
        self.output_object_file.truncate()
    '''
    Add adds an inference to class/object property
    i~ index to insert inference
    item_to_edit~Class/object property to add inference to
    alt_item_to_edit ~alternative format name of class/object property to be edited
    edit ~ inference
    line ~ the line to compare to determine if inference added at that point
    '''
    def add(self, i, item_to_edit, alt_item_to_edit, edit, line):
        #print("adding deduction")
        if (item_to_edit in line) or (alt_item_to_edit in line):  # with iri or without iri
            ed = edit.decode('ascii').strip()
            new_edit = b'        '+ ed.encode('ascii')+'\n'.encode('ascii')
            self.list_file.insert(i+1, new_edit)
            self.dict_deduction_line[edit] = i+1
