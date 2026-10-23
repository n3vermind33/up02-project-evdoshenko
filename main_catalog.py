import tkinter as tk
from tkinter import ttk
from config import COLOR_SECONDARY_BG, FONT_FAMILY, FONT_SIZE_TITLE
from config import APP_TITLE
import databases as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from db_products import get_all_products



class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")

        # Иконка приложения
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
        # Шапка с логотипом и заголовком
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Логотип (слева) — с сохранением пропорций!
        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок (по центру)
        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            bg=COLOR_SECONDARY_BG).pack(expand=True)

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
        products = get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
