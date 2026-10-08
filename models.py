"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар."""

    def __init__(self, product_id, country, city, price, quantity, duration):
        self.id = product_id
        self.country = country
        self.city = city
        self.price = float(price)
        self.quantity = int(quantity)
        self.duration = duration
        
    def discounted_price(self):
        return self.price * 0.90

    def total(self):
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        return self.price * (1 - discount_percent / 100)

    def price_with_discount_auto(self, date=None):
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        return self.quantity > 0

    def info(self):
        return (
            f"{self.country} ({self.city}): "
            f"{self.duration} дн. | "
            f"{self.price} руб. × {self.quantity} = {self.total():.2f} руб. "
            f"({self.indicator()})"
        )
    
    


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product
        self.quantity = int(quantity)

    def total(self):
        return self.product.price * self.quantity

    def with_discount(self, discount_percent):
        return self.total() * (1 - discount_percent / 100)

    def is_available(self):
        return self.product.quantity >= self.quantity

    def info(self):
        p = self.product
        return (
            f"Заказ №{self.id} от {self.date}: {self.client} — "
            f"{p.country} ({p.city}), {p.duration} дн. × {self.quantity} "
            f"= {self.total():.2f} руб."
        )

    def order_info(self):
        return f"Заказ №{self.id} от {self.date}: {self.client}"


if __name__ == "__main__":
    p = Product(2, "Турция", "Анталья", 15000, 3, 7)
    date = datetime(2026, 10, 15)
    print(f"Базовая цена: {p.price}")
    print(f"Со скидкой: {p.price_with_discount_auto(date)}")