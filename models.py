"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар."""

    def __init__(self, product_id, country, city, price, quantity, duration):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        """
        self.id = product_id
        self.country = country
        self.city = city
        self.price = price
        self.quantity = quantity
        self.duration = duration

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.country} ({self.city}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )
