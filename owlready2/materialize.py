from owlready2.namespace import _open_onto_file

class Materialize:
    def __init__(self, deductions, input_file, output_file):
        self.deductions = deductions
        self.input_file = input_file
        self.output_file = output_file
        self.base_iri = '''<?xml version="1.0"?>'''
        self.list_file = []
        self.dict_deduction_line = {}#{deduction.edit, line number where it was added}
        self.input_object_file = _open_onto_file(self.base_iri, self.input_file, mode="rb", only_local=False)
        self.output_object_file = _open_onto_file(self.base_iri, self.output_file, mode="rb+", only_local=False)

    def load_input_file(self):
        for line in self.input_object_file:
            self.list_file.append(line)


    def materialize_deductions(self):
        #add deduction in list encapsulating file
        for i, line in enumerate(self.list_file):
            #print("line: ---->")
            #print(line)
            for deduction in self.deductions:
                index = deduction.item_to_edit.rfind('#')
                refact_item_to_edit = deduction.item_to_edit[:7]+deduction.item_to_edit[index:]
                '''this is where we need to differentiate between types ,below 2 lines works for entity & some relationship subsumption, inconsistency tags
                if 'subclass' : self.add
                inherit cardinality restrictions(from parent class)
                domain and ranges*?
                if 'inconsistent' : self.add
                if object property and object property doesn't exist: self.add
                if object property and object property does exist: self.replace
                '''
                #print("line: ---->")
                #print(line)
                #print("deduction----->")
                #print(deduction)
                #UP NEXT if equivalent class, then add all subclasses of equivalent to its corresponding class
                if "equivalentClass" in deduction.edit:#find all classes that reference the equivalent class and reference the other, same for object properties
                    self.add(i, deduction.item_to_edit.encode('utf_8'), refact_item_to_edit.encode('utf_8'), deduction.edit.encode('utf_8'), line)
                if "subClassOf" in deduction.edit:#entity subsumption
                    self.add(i, deduction.item_to_edit.encode('utf_8'), refact_item_to_edit.encode('utf_8'), deduction.edit.encode('utf_8'), line)
                if ("owl#Nothing" in deduction.edit) and ("Class" in deduction.edit):
                    print("inconsistent class")
                    self.add(i, deduction.item_to_edit.encode('utf_8'), refact_item_to_edit.encode('utf_8'), "<!--DEDUCTION-->\n<!--INCONSISTENT CLASS-->\n".encode('utf_8'), line)
        #print("\n\nPRINTING FINAL FILE\n\n*_*_*_*_*_*_*_*_*_*_*_*_*_*_*\n\n")
        #self.write_to_RDFXML()
        #for line in self.list_file:
            #self.output_object_file.write(line)

    def write_to_RDFXML(self):
        for line in self.list_file:
            self.output_object_file.write(line)
            #print(line)
        print("deductions have been materialized")
        '''    
                print()
                print("line\n-----")
                print(line)
                print("refact item to edit\n------")
                print(refact_item_to_edit)
                print("item to edit\n-------")
                print(deduction.item_to_edit)
            '''

    def add(self, i, item_to_edit, alt_item_to_edit, edit, line):
        if (item_to_edit in line) or (alt_item_to_edit in line):  # with iri or without iri
            self.list_file.insert(i+1, edit)
            self.dict_deduction_line[edit] = i+1
            for i in self.dict_deduction_line:
                print('dictionary')
                print(edit)
                print(self.dict_deduction_line[edit])

    def repref(self, i, item_to_edit, alt_item_to_edit, eq_item ):
        #exclude item to edit when adding
        #print(eq_item)
        #print(alt_item_to_edit)
        print()

    def writeToLog(self, item_to_edit, alt_item_to_edit,case):
        log = open(self.output_file[:4]+".txt", "w+")
        log.write()