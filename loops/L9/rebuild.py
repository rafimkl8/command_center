class ShoppingCart:
    def __init__(self, category_name, items):
        self.category_name = category_name
        self.items = items

    def __str__(self):
        return f"Catagory Name: {self.category_name}, Total {len(self.items)} items here!"

    def __repr__(self):
        return f"ShoppingCart(category_name={self.category_name})"

    def __eq__(self, other_cart):
        return self.category_name == other_cart.category_name

    def __len__(self):
        return len(self.items)


cart1 = ShoppingCart("Electronics", ["Mobile", "TV"])
cart2 = ShoppingCart("Electronics", ["Smart-Watch", "Tab", "Earphone"])
cart3 = ShoppingCart("Home", ["Frying Pan", "Olive Oil"])

print(cart1)
print(cart2)
print(repr(cart1))
print(repr(cart2))
print(cart1 == cart2)
print(cart2 == cart3)
print(len(cart1))
print(len(cart2))
