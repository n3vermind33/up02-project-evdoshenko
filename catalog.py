import tkinter as tk

from config import (
	COLOR_MAIN_BG, COLOR_HIGHLIGHT,
	FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER
)
from resources import get_product_image
from db_products import get_all_products


class ToolTip:
	"""Всплывающая подсказка при наведении на виджет."""
	def __init__(self, widget, text):
		self.widget = widget
		self.text = text
		self.tip = None
		widget.bind("<Enter>", self.show)
		widget.bind("<Leave>", self.hide)

	def show(self, event=None):
		x = self.widget.winfo_rootx() + 20
		y = self.widget.winfo_rooty() + 20
		self.tip = tk.Toplevel(self.widget)
		self.tip.wm_overrideredirect(True)
		self.tip.geometry(f"+{x}+{y}")
		tk.Label(self.tip, text=self.text, background="lightyellow",
				 relief="solid", borderwidth=1, justify="left",
				 padx=6, pady=4).pack()

	def hide(self, event=None):
		if self.tip:
			self.tip.destroy()
			self.tip = None


def create_product_card(parent, product):
	"""Создаёт карточку товара по макету."""
	qty = product.quantity
	bg_color = _get_card_color(qty)

	card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
	card.pack(fill="x", padx=10, pady=5)

	_add_image(card, product, bg_color)
	_add_text_info(card, product, bg_color, qty)

	tooltip_text = (
		f"Страна: {product.country}\n"
		f"Город: {product.city}\n"
		f"Длительность: {product.duration}\n"
		f"Цена: {product.price} руб.\n"
		f"Количество: {product.quantity}"
	)
	ToolTip(card, tooltip_text)

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


def format_price(price):
	"""Форматирует цену с разделителем тысяч."""
	return f"{float(price):,.0f}".replace(",", " ")


def format_duration(duration):
	"""Склоняет слово 'день' в зависимости от числа."""
	try:
		d = int(duration)
		if d % 10 == 1 and d % 100 != 11:
			return f"{d} день"
		elif 2 <= d % 10 <= 4 and not (12 <= d % 100 <= 14):
			return f"{d} дня"
		else:
			return f"{d} дней"
	except (ValueError, TypeError):
		return f"{duration} дн."


def _add_text_info(card, product, bg_color, qty):
	"""Добавляет текстовую информацию о туре."""
	text_frame = tk.Frame(card, bg=bg_color)
	text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

	country  = product.country  if product.country  else "[Страна не указана]"
	city     = product.city     if product.city     else "[Город не указан]"
	duration = product.duration if product.duration else "[Длительность не указана]"
	price    = product.price    if product.price is not None else 0

	_add_label(text_frame, f"{country} | {city}",
			   bg_color, bold=True, size=FONT_SIZE_HEADER)
	
	_add_label(text_frame, f"Длительность: {format_duration(duration)}", bg_color)
	
	_add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
	_add_label(text_frame, f"{format_price(price)} руб.",
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


def matches_query(product, query):
	"""Проверяет, содержит ли товар поисковый запрос (по нескольким полям)."""
	if not query:
		return True
	query = query.lower().strip()
	return (
		query in str(product.country).lower() or
		query in str(product.city).lower() or
		query in str(product.duration).lower()
	)


def group_by_country(products):
	"""Группирует товары по странам (категориям)."""
	groups = {}
	for p in products:
		cat = p.country if p.country else "[Без категории]"
		groups.setdefault(cat, []).append(p)
	return groups


class Pagination:
	"""Класс для разбивки списка товаров на страницы."""
	def __init__(self, products, page_size=5):
		self.products = products
		self.page_size = page_size
		self.current_page = 0

	def get_page(self):
		start = self.current_page * self.page_size
		end = start + self.page_size
		return self.products[start:end]

	def next(self):
		if (self.current_page + 1) * self.page_size < len(self.products):
			self.current_page += 1

	def prev(self):
		if self.current_page > 0:
			self.current_page -= 1