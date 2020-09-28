from owlready2 import *
from owlready2.materialize import Materialize
from owlready2.preprocess import Preprocess


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
    def manage(self):
        print("Please review the changes that have been made to your model below.")
        for i, deduction in enumerate(self.materialize.deductions):
            if "subClassOf" in deduction.edit:  # entity subsumption
                #print("subclass")
                self.e_s_manage((i+1),deduction)
        #send all again to reasoner and inform of consequences

    def e_s_manage(self, i, deduction):
        print("deduction.edit")
        print(deduction.edit)
        print("deduction.itemtoedit")
        print(deduction.item_to_edit)
        print("type")
        print(deduction.type)
        print("\n\n\n\n\n")

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
            #delete subclass and all references to it in entire file
            self.remove_subclass(deduction)
            print(self.refact_i_t_e + " has been removed. All constraints referencing the class have also been removed")
        if send_back:
            self.resend()
    def resend(self):
        test_file_path = "/Users/mandisabaleni/PycharmProjects/MaterializationOfDeductions/testsamplemodels"
        input_owl_name = self.materialize.output_file[self.materialize.output_file.rindex("/") + 1:]  # "EntitySubsumption_i"#"wrapper_removesubclass.owl"#
        print("YO000")
        print(input_owl_name)
        print("Y0000")
        deductions_owl_name = "temp2.owl"
        output_owl_name = self.new_output_file  # change

        onto_path.append(test_file_path)
        re_onto = get_ontology(input_owl_name)
        re_onto.load()
        print("RESENDING")
        print(list(re_onto.classes()))
        print(list(re_onto.object_properties()))
        print("AFTER RESENDING")

        test_onto = get_ontology(deductions_owl_name)
        with test_onto:  # change back to test_onto
            sync_reasoner()
        print("after reasoning TAKE 2")
        test_onto.save()  # change back to test_onto

        reprep = Preprocess(test_file_path + "/" + input_owl_name, test_file_path + "/" + deductions_owl_name,
                            test_file_path + "/" + output_owl_name)
        reprep.find_items()
        rematerial = Materialize(reprep.deductions, test_file_path + "/" + input_owl_name,
                                 test_file_path + "/" + output_owl_name, reprep)
        rematerial.load_input_file()
        rematerial.materialize_deductions()
        rematerial.write_to_RDFXML()

    def remove_deduction(self, deduction):
        print(deduction.edit.encode('ascii'))
        i = self.materialize.dict_deduction_line[deduction.edit.encode('ascii')]
        print('\n\n TO BE DELETED\n\n')
        print(self.materialize.list_file[i:i+1])
        print()
        print("printing file BEFORE deduction removed")
        for line in self.materialize.list_file:
            print(line)
        del self.materialize.list_file[i:i+1]
        print("printing file AFTER deduction removed")
        for line in self.materialize.list_file:
            print(line)

    def remove_subclass(self, deduction):
        #print(deduction.item_to_edit)
        index = deduction.item_to_edit.rindex("#")
        parent_to_remove = deduction.item_to_edit[index:deduction.item_to_edit.rindex("\"")].strip()
        #print(parent_to_remove)

        #GETTING CONTENTS OF PARENT
        par_contents = ''
        delete_index = []
        for i, par in enumerate(self.preprocess.items):
            #check if parent has no children, delete the object property
            if parent_to_remove in par.name:
                par_contents = par.assemble()
                #DELETING PARENT
                print("DELETING PARENT")
                print(self.preprocess.items[i].name)

                delete_index.append(i)
                print(i)

        #DELETING PARENT CONT.
        if delete_index:
            for j in delete_index:
                del self.preprocess.items[j]
        print('FINISHED DELETING PARENT')

        #INHERITING TO SUBCLASSES
        for class_item in self.preprocess.items:
            if parent_to_remove in class_item.parent:
                class_item.assemble()
                class_item.inherit(par_contents)
                class_item.full_item()
                #DELETING SUBCLASS REFERENCES TO PARENT
                class_item.del_in_item('#'+self.refact_i_t_e)
            else:
                class_item.assemble()
                class_item.full_item()
        #self.preprocess.items_original_file()
        for obj_item in self.preprocess.obj_items:
            obj_item.assemble_obj()
            obj_item.full_item()
        self.materialize.write_to_RDFXML_via_items(self.preprocess.items, self.preprocess.obj_items)








    '''
    def onlysubclass(self):
        print("method that checks removing for only subclass. currently not implemented")
    '''

