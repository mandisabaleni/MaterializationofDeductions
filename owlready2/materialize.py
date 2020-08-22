from owlready2.namespace import _open_onto_file

class Materialize:
    def __init__(self, deductions, input_file, output_file):
        self.deductions = deductions
        self.input_file = input_file
        self.output_file = output_file
        self.base_iri = '''<?xml version="1.0"?>'''
        self.list_file = []
        self.input_object_file = _open_onto_file(self.base_iri, self.input_file, mode="rb", only_local=False)
        self.output_object_file = _open_onto_file(self.base_iri, self.output_file, mode="rb+", only_local=False)

    def load_input_file(self):
        for line in self.input_object_file:
            self.list_file.append(line)


    def materialize_deductions(self):
        #add deduction in list encapsulating file
        for i, line in enumerate(self.list_file):
            for deduction in self.deductions:
                index = deduction.item_to_edit.rfind('#')
                refact_item_to_edit = deduction.item_to_edit[:7]+deduction.item_to_edit[index:]
                '''this is where we need to differentiate between types below 2 lines works for entity & some relationship subsumption'''
                if (deduction.item_to_edit.encode('utf_8') in line) or (refact_item_to_edit.encode('utf_8') in line):#with iri or without iri
                    self.list_file.insert(i+1, deduction.edit.encode('utf_8'))
        for line in self.list_file:
            self.output_object_file.write(line)
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