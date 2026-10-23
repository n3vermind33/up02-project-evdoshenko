import tkinter as tk

from config import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER
)
from resources import get_product_image
from db_products import get_all_products


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product.image, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о туре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Значения с проверкой на пустоту (крайние случаи)
    country  = product.country  if product.country  else "[Страна не указана]"
    city     = product.city     if product.city     else "[Город не указан]"
    duration = product.duration if product.duration else "[Длительность не указана]"
    price    = product.price    if product.price is not None else 0

    # Заголовок: «Страна | Город»
    _add_label(text_frame, f"{country} | {city}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    # Длительность тура
    _add_label(text_frame, f"Длительность: {duration}", bg_color)
    # Количество (с индикатором «много/мало»)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    # Цена
    _add_label(text_frame, f"{price} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text,
             font=(FONT_FAMILY, size, "bold" if bold else "normal"),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    return "много" if qty > 5 else "мало"