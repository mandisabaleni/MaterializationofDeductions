from owlready2.deduction import Deduction
from owlready2.namespace import _open_onto_file

class Wrapper:
    def __init__(self, mod):
        self.materialize = mod
        self._1 = "a) Accept\n"
        self._2 = "b) Decline (remove constraint)\n"
        self._3 = "c) Remove constraint\n"
        self._4 = "c) Remove subclass\n"
        self._5 = "d) Remove relationship\n"
        self.tab = "   "
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
        refact_i_t_e = deduction.item_to_edit[index_i_t_e+1:len(deduction.item_to_edit)-2]
        index_e = deduction.edit.rfind('#')
        refact_e = deduction.edit[index_e+1:len(deduction.edit)-4]
        print(self.tab + refact_i_t_e + " is a subclass of " + refact_e )
        print(self.tab + "\n" +self.tab + "Please select what to do with the deduction from the choices below:"+"\n"+self.tab + "(Reference deduction by number. E.g 1 a")
        print(self.tab + self._1 +self.tab +  self._2 +self.tab + self._4)
        choice = input()
        if choice == ("1 a"):
            print("Deduction accepted.")
        if choice == ("1 b"):
            self.remove_deduction(deduction)
            print("Deduction has been removed")
        if choice == ("1 c"):
            #delete subclass and all references to it in entire file
            print(refact_i_t_e + " has been removed. All references to the class have also been removed")

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