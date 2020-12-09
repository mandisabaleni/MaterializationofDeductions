from owlready2 import *
from owlready2.Extension_MOD.materialize import Materialize
from owlready2.Extension_MOD.preprocess import Preprocess
'''
Wrapper initiates text user interface to manage the decisions of users on made inferences. This includes removing 
inference, accepting it, or removing a deduced subclass
'''
class Wrapper:
    def __init__(self, mod, prep):
        self.materialize = mod
        self.preprocess = prep
        self.new_output_file = "EntitySubsumption_o2.owl"
        self._1 = "a) Accept\n"
        self._2 = "b) Decline (remove constraint)\n"
        self._3 = "c) Remove subclass\n"
        self._4 = "d) Remove relationship\n"
        self.tab = "   "
        self.refact_i_t_e = ''
    '''
    Manage initiates wrapper functionality
    '''
    def manage(self):
        print("Please review the changes that have been made to your model below.")
        for i, deduction in enumerate(self.materialize.deductions):
            if "subClassOf" in deduction.edit:
                self.e_s_manage((i+1),deduction)

    '''
    E_s_manage alerts user of added constraints and asks them to make a choice
    deduction ~ the inference that was made to be displayed to user
    i ~ number of inference
    '''
    def e_s_manage(self, i, deduction):
        print(str(i) +". " +"SUBCLASS constraint was added:\n")
        index_i_t_e = deduction.item_to_edit.rfind('#')
        self.refact_i_t_e = deduction.item_to_edit[index_i_t_e+1:len(deduction.item_to_edit)-2]
        index_e = deduction.edit.rfind('#')
        refact_e = deduction.edit[index_e+1:len(deduction.edit)-4]
        print(self.tab + self.refact_i_t_e + " is a subclass of " + refact_e )
        print(self.tab + "\n" +self.tab + "Please select what to do with the deduction from the choices below:"+"\n"+self.tab + "( E.g a")
        print(self.tab + self._1 +self.tab +  self._2 +self.tab + self._3)
        choice = input()
        send_back = False
        if choice == ("a"):#deduction accepted
            print("Deduction accepted.")
        if choice == ("b"):#remove constraint
            send_back = True
            self.remove_deduction(deduction)
            print("Deduction has been removed")
        if choice == ("c"):#remove subclass
            send_back = True
            self.remove_subclass(deduction)
            print(self.refact_i_t_e + " has been removed. All constraints referencing the class have also been removed")
        if send_back:
            print()

    '''
    Resend resends OWL back to reasoner after user makes choice
    (introduced bug)
    '''
    def resend(self):
        test_file_path = "/MaterializationOfDeductions/testsamplemodels"
        input_owl_name = self.materialize.output_file[self.materialize.output_file.rindex("/") + 1:]
        deductions_owl_name = "temp2.owl"
        output_owl_name = self.new_output_file  # change

        onto_path.append(test_file_path)
        re_onto = get_ontology(input_owl_name)
        re_onto.load()

        test_onto = get_ontology(deductions_owl_name)
        with test_onto:
            sync_reasoner()
        test_onto.save()

        reprep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name,test_file_path + "/" + output_owl_name)
        reprep.find_items()
        rematerial = Materialize(reprep.deductions, test_file_path + "/" + input_owl_name,test_file_path + "/" + output_owl_name, reprep)
        rematerial.load_input_file()
        rematerial.materialize_deductions()
        rematerial.write_to_RDFXML()
    '''
    Remove_deduction removes an inferred constraint from the OWL file
    deduction ~ the infered constraint
    '''
    def remove_deduction(self, deduction):
        ed = deduction.edit.strip()
        new_edit = b'        ' + ed.encode('ascii') + '\n'.encode('ascii')
        i = self.materialize.dict_deduction_line[deduction.edit.encode('ascii')]
        del self.materialize.list_file[i:i+1]
        self.materialize.deleteContent()
        self.materialize.write_to_RDFXML()
    '''
    Remove_subclass removes the class inferred as a subclass of another
    deduction ~ the inferred class
    '''
    def remove_subclass(self, deduction):
        index = deduction.item_to_edit.rindex("#")
        parent_to_remove = deduction.item_to_edit[index:deduction.item_to_edit.rindex("\"")].strip()

        #GETTING CONTENTS OF PARENT
        par_contents = ''
        delete_index = []
        for i, par in enumerate(self.materialize.items):
            #check if parent has no children, delete the object property
            if parent_to_remove in par.name:
                par_contents = par.assemble()
                #DELETING PARENT
                delete_index.append(i)

        #DELETING PARENT CONT.
        if delete_index:
            for j in delete_index:
                del self.materialize.items[j]

        #INHERITING TO SUBCLASSES
        bool_children = False
        for class_item in self.materialize.items:
            if parent_to_remove in class_item.parent:
                bool_children = True
                class_item.assemble()
                if par_contents not in class_item.contents:
                    class_item.inherit(par_contents)
                class_item.full_item()
                #DELETING SUBCLASS REFERENCES TO PARENT
                class_item.del_in_item('#'+self.refact_i_t_e)
            else:
                class_item.assemble()
                class_item.full_item()

        #DELETING RELATIONSHIPS
        delete_index_o = []
        if bool_children == False:
            for i, obj in enumerate(self.materialize.obj_items):
                if parent_to_remove in obj.domain:
                    delete_index_o.append(i)
        for j in delete_index_o:
                del self.materialize.obj_items[j]

        for obj_item in self.materialize.obj_items:
            obj_item.assemble_obj()
            obj_item.full_item()

        self.materialize.list_file.clear()

        self.materialize.list_file.append(self.materialize.header.encode('ascii'))
        self.materialize.list_file.append(self.materialize.CLASS_HEADER.encode('ascii'))
        for class_item in self.materialize.items:
            class_item.to_list()
            for line in class_item.full_list:
                self.materialize.list_file.append((line+'\n').encode('ascii'))
        self.materialize.list_file.append(self.materialize.OBJ_PROP_HEADER.encode('ascii'))
        for obj_item in self.materialize.obj_items:
            obj_item.to_list()
            for line in obj_item.full_list:
                self.materialize.list_file.append((line+'\n').encode('ascii'))
        self.materialize.list_file.append('</rdf:RDF>'.encode('ascii'))

        self.materialize.deleteContent()
        self.materialize.write_to_RDFXML()













