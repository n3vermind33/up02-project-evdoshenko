"""Проверка класса Product."""
from models import Product


# Создаём один товар вручную
p = Product(
    product_id=1,
    country="Турция",
    city="Анталья",
    price=50000,
    quantity=2,
    duration=14
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
