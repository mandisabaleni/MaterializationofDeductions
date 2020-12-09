'''This class defines an encapsualtes an OWL class or object property in an Item object
It handles inheriting cardianlity constraints on object properties, disjointness, equivalence
and covering constraints. The class is also responsible for reconstructing a class or object property
in OWL syntax
'''
class Item:
    def __init__(self, name):
        self.name = name
        self.eq = ''
        self.card_restr = ''
        self.parent = ''
        self.disjoint = ''
        self.covering = ''

        self.bool_eq = False
        self.bool_card_restr = False
        self.bool_parent = False
        self.bool_disjoint = False
        self.bool_covering = False

        self.contents = ''
        self.full = ''
        self.full_list = []

        self.domain = ''
        self.range = ''

        self.bool_domain = ''
        self.bool_range = ''
    '''
    Aseemble collates all constraints of the class into a stored string
    '''
    def assemble(self):
        if self.bool_parent:
            self.contents += self.parent
        if self.bool_eq:
            self.contents += self.eq
        if self.bool_card_restr:
            self.contents += self.card_restr
        if self.bool_disjoint:
            self.contents += self.disjoint
        if self.bool_covering:
            self.contents += self.covering
        return self.contents
    '''
    Aseemble collates all constraints of the object property into a stored string
    '''
    def assemble_obj(self):
        if self.bool_parent:
            self.contents += self.parent
        if self.bool_domain:
            self.contents += self.domain
        if self.bool_range:
            self.contents += self.range

    '''
    Inherit inherits all constraints from a parent class/object property and concatenates them with own constraints
    par_contents ~ the constraints of parent
    '''
    def inherit(self, par_contents):
        self.contents += par_contents

    '''
    Full_item amends the constraints of a class/object property to its name(iri) to be a full OWL RDF/XML-specified
    class/object property
    '''
    def full_item(self):
        if "<owl:Class rdf:about=" in self.name:
            if self.contents == '':
                self.full += self.name + self.contents + "\n"
            else:
                self.full += self.name + self.contents + "    </owl:Class>\n\n"
        if "<owl:ObjectProperty rdf:about=" in self.name:
            if self.contents == '':
                self.full += self.name + self.contents + "\n"
            else:
                self.full += self.name + self.contents + "    </owl:ObjectProperty>\n\n"
        return self.full

    '''
    To_list reverts a class/object property in string to a list
    '''
    def to_list(self):
        self.full_list = self.full.split("\n")

    '''
    List_to_string reverts a class/object property encapsulated in a list to a string
    '''
    def list_to_string(self):
        self.full = ''
        for line in self.full_list:
            self.full += line +"\n"
    '''
    Del_in_item deletes a given string in within the body of constraints of a class/object propety
    str ~ string to be deleted
    '''
    def del_in_item(self, str):
        self.to_list()
        for i, line in enumerate(self.full_list):
            if str in line:
                del self.full_list[i]
        self.list_to_string()