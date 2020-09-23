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
