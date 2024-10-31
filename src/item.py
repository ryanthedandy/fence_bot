class Item:
    def __init__(self):
        self.name = None
        self.rarity = None
        self.attributes = []
        self.owner = None
        self.price = None
        self.crafted_variants = 0
        self.craft_buffer = 0
        self.is_listed = False
        self.is_sold = False
        self.in_stash = True
        self.item_panel = None
        self.slot = None


    def __str__ (self):
        return f"""This item is {self.name} of {self.rarity} rarity, with the attributes of {self.attributes}. 
        It is owned by {self.owner} and costs {self.price}. It has {self.crafted_variants} crafted variants."""

    def to_json(self):
        return {
            "name": self.name,
            "rarity": self.rarity,
            "attributes": self.attributes,
            "owner": self.owner,
            "price": self.price,
            "crafted_variants": self.crafted_variants,
            "is_listed": self.is_listed,
            "is_sold": self.is_sold,
            "in_stash": self.in_stash,
            "item_panel": self.item_panel,
            "slot": self.slot
        }

    @classmethod
    def from_json(cls, data):
        item = cls()
        item.name = data["name"]
        item.rarity = data["rarity"]
        item.attributes = data["attributes"]
        item.owner = data["owner"]
        item.price = data["price"]
        item.crafted_variants = data["crafted_variants"]
        item.is_listed = data["is_listed"]
        item.is_sold = data["is_sold"]
        item.in_stash = data["in_stash"]
        item.item_panel = data["item_panel"]
        item.slot = data["slot"]
        return item
