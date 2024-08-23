class Item:
    def __init__(self):
        self.name = None
        self.rarity = None
        self.attributes = []
        self.owner = None
        self.price = None
        self.crafted_variants = 0
        self.is_listed = False
        self.is_sold = False
        self.in_stash = True
        self.item_panel = None
        self.slot = None


    def __str__ (self):
        return f"""This item is {self.name} of {self.rarity} rarity, with the attributes of {self.attributes}. 
        It is owned by {self.owner} and costs {self.price}. It has {self.crafted_variants} crafted variants."""



    