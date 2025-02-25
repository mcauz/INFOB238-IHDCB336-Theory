from models import Category, Flower, CartItem, Cart, User


categories = [
    Category(id=0, name="Red flowers"),
    Category(id=1, name="Orange flowers"),
    Category(id=2, name="White flowers")
]

flowers = [
    Flower(id=0, name="Gerbera", image="gerbera.jpeg", unit_price=1, quantity=100, category=categories[0]),
    Flower(id=1, name="Red rose", image="red-rose.jpeg", unit_price=3, quantity=60, category=categories[0]),
    Flower(id=2, name="Lily", image="lily.jpeg", unit_price=5, quantity=50, category=categories[1]),
    Flower(id=3, name="Daisy", image="daisy.jpeg", unit_price=2, quantity=70, category=categories[2])
]

cart_items = [
    [],
]

carts = [
    Cart(id=0, items=cart_items[0])
]

users = [
    User(id=0, username="Maxime", password="Maxime", token=300, cart=carts[0])
]