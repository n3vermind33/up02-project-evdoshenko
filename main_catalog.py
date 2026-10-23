import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_SECONDARY_BG, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_HEADER
from config import APP_TITLE
import databases as db
from catalog import create_product_card, matches_query, group_by_country, Pagination
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from db_products import get_all_products


class CatalogWindow:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title(APP_TITLE)
		self.root.geometry("900x700")

		self.current_page = 0
		self.page_size = 5  # По 5 товаров на страницу

		self.set_icon()
		self.build_ui()
		self.load_products()

	def set_icon(self):
		"""Устанавливает иконку приложения (кроссплатформенно)."""
		try:
			self._icon = tk.PhotoImage(file=PATH_ICON)
			self.root.iconphoto(True, self._icon)
		except Exception as e:
			print(f"Не удалось установить иконку: {e}")

	def build_ui(self):
		# Шапка
		header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
		header.pack(side="top", fill="x")
		header.pack_propagate(False)

		# Логотип
		logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
		if logo:
			logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
			logo_label.image = logo
			logo_label.pack(side="left", padx=15)
		else:
			tk.Label(header, text="[ЛОГОТИП]",
					 bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

		# Заголовок
		tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
			font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
			bg=COLOR_SECONDARY_BG).pack(expand=True)

		# Счётчик (правый край)
		self.count_label = tk.Label(
			header, text="Товаров: 0",
			bg=COLOR_SECONDARY_BG,
			font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")
		)
		self.count_label.pack(side="right", padx=15)

		# Кнопка «Экспорт»
		self.export_btn = tk.Button(
			header, text="Экспорт",
			command=self.export_catalog,
			font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")
		)
		self.export_btn.pack(side="right", padx=5)

		# Поле поиска
		self.search_var = tk.StringVar()
		self.search_entry = tk.Entry(
			header, textvariable=self.search_var, width=15,
			font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")
		)
		self.search_entry.pack(side="right", padx=5)
		tk.Label(header, text="Поиск:",
				 bg=COLOR_SECONDARY_BG,
				 font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")).pack(side="right")

		# Сортировка
		tk.Label(header, text="Сортировка:",
				 bg=COLOR_SECONDARY_BG,
				 font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")).pack(side="right", padx=(10, 0))

		self.sort_var = tk.StringVar(value="По умолчанию")
		self.sort_combo = ttk.Combobox(
			header,
			textvariable=self.sort_var,
			state="readonly",
			width=15,
			values=["По умолчанию", "Цена ↑", "Цена ↓", "Длительность ↑"],
			font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal")
		)
		self.sort_combo.pack(side="right", padx=(5, 0))

		# Живой поиск и смена сортировки. При изменении сбрасываем на 1-ю страницу!
		self.search_var.trace_add("write", lambda *a: self.reset_and_refresh())
		self.sort_var.trace_add("write", lambda *a: self.reset_and_refresh())

		# Нижняя панель (Пагинация)
		footer = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=50)
		footer.pack(side="bottom", fill="x")
		footer.pack_propagate(False)

		self.btn_prev = tk.Button(footer, text="<- Назад", command=self.prev_page,
								  font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal"))
		self.btn_prev.pack(side="left", padx=20, pady=10)

		self.btn_next = tk.Button(footer, text="Вперёд ->", command=self.next_page,
								  font=(FONT_FAMILY, FONT_SIZE_NORMAL, "normal"))
		self.btn_next.pack(side="right", padx=20, pady=10)

		self.lbl_page = tk.Label(footer, text="Стр. 1 из 1",
								 bg=COLOR_SECONDARY_BG,
								 font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"))
		self.lbl_page.pack(side="top", pady=15)

		# Область с прокруткой
		self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
		scrollbar = ttk.Scrollbar(self.root, orient="vertical",
								   command=self.canvas.yview)
		self.catalog_frame = tk.Frame(self.canvas, bg="white")
		self.catalog_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		)
		self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=scrollbar.set)
		self.canvas.pack(side="left", fill="both", expand=True)
		scrollbar.pack(side="right", fill="y")

	def load_products(self):
		"""Первичная загрузка каталога."""
		self.refresh_catalog()

	def reset_and_refresh(self):
		"""Сбрасывает на первую страницу и обновляет каталог."""
		self.current_page = 0
		self.refresh_catalog()

	def next_page(self):
		"""Переход на следующую страницу."""
		self.current_page += 1
		self.refresh_catalog()

	def prev_page(self):
		"""Переход на предыдущую страницу."""
		self.current_page -= 1
		self.refresh_catalog()

	def refresh_catalog(self):
		"""Перерисовывает каталог с учетом пагинации, фильтрации и сортировки."""
		query = self.search_var.get() if hasattr(self, "search_var") else ""
		sort_order = self.sort_var.get() if hasattr(self, "sort_var") else "По умолчанию"

		products = get_all_products()
		filtered = [p for p in products if matches_query(p, query)]

		# 1. Сортировка
		if sort_order == "Цена ↑":
			filtered.sort(key=lambda p: float(p.price))
		elif sort_order == "Цена ↓":
			filtered.sort(key=lambda p: float(p.price), reverse=True)
		elif sort_order == "Длительность ↑":
			filtered.sort(key=lambda p: int(p.duration) if str(p.duration).isdigit() else 0)

		# 2. Пагинация
		paginator = Pagination(filtered, page_size=self.page_size)
		paginator.current_page = self.current_page
		
		# Проверка: если текущая страница вышла за пределы (например, из-за поиска)
		max_page = max(0, (len(filtered) - 1) // self.page_size) if filtered else 0
		if paginator.current_page > max_page:
			paginator.current_page = max_page
		if paginator.current_page < 0:
			paginator.current_page = 0
			
		self.current_page = paginator.current_page
		page_items = paginator.get_page()

		# 3. Очистка старых карточек
		for w in self.catalog_frame.winfo_children():
			w.destroy()

		# 4. Группировка и отрисовка (только товаров с текущей страницы)
		grouped = group_by_country(page_items)
		
		for country in grouped.keys():
			tk.Label(self.catalog_frame, text=f"=== {country} ===",
					 font=(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
					 bg=COLOR_SECONDARY_BG, fg="black").pack(fill="x", padx=10, pady=(10, 5))
					 
			for p in grouped[country]:
				create_product_card(self.catalog_frame, p)

		# 5. Обновление интерфейса (счетчик, кнопки, номер страницы)
		self.count_label.config(text=f"Товаров: {len(filtered)}")
		self.lbl_page.config(text=f"Стр. {self.current_page + 1} из {max_page + 1}")
		
		# Блокируем кнопки, если некуда идти
		if self.current_page <= 0:
			self.btn_prev.config(state="disabled")
		else:
			self.btn_prev.config(state="normal")
			
		if self.current_page >= max_page:
			self.btn_next.config(state="disabled")
		else:
			self.btn_next.config(state="normal")

	def export_catalog(self):
		"""Экспортирует каталог в CSV-файл."""
		products = get_all_products()
		if not products:
			messagebox.showwarning("Экспорт", "Каталог пуст — нечего экспортировать.")
			return

		base_dir = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(base_dir, "catalog_export.csv")

		with open(path, "w", encoding="utf-8-sig", newline="") as f:
			writer = csv.writer(f, delimiter=";")
			writer.writerow(["ID", "Страна", "Город", "Длительность", "Цена", "Количество"])
			for p in products:
				writer.writerow([
					getattr(p, "product_id", getattr(p, "id", "")),
					p.country, p.city, p.duration, p.price, p.quantity,
				])

		messagebox.showinfo("Экспорт", f"Сохранено в:\n{path}")
		print(f"✅ Экспортировано в {path}")

	def run(self):
		self.root.mainloop()


if __name__ == "__main__":
	CatalogWindow().run()