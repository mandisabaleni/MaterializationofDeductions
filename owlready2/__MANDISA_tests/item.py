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

        #for OBJECT PROPERTIES
        self.domain = ''
        self.range = ''
        #functional
        #transitive
        #inverse functional

        self.bool_domain = ''
        self.bool_range = ''

    #assemble classes
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

    def assemble_obj(self):
        if self.bool_parent:
            self.contents += self.parent
        if self.bool_domain:
            self.contents += self.domain
        if self.bool_range:
            self.contents += self.range
    def inherit(self, par_contents):
        #check if par_contents in contents already
        self.contents += par_contents

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
        print( self.full)
        return self.full

    def to_list(self):
        #DO IN BINARY?
        self.full_list = self.full.split("\n")

    #rewrites full string using whats currently in the list
    def list_to_string(self):
        self.full = ''
        for line in self.full_list:
            self.full += line +"\n"

    def del_in_item(self, str):
        self.to_list()
        for i, line in enumerate(self.full_list):
            if str in line:
                del self.full_list[i]
        self.list_to_string()

