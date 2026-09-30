"""Загрузка товаров из БД с расширенным выводом."""
import sqlite3
from config import DB_PATH


def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products


def get_products_by_city(city):
    """Товары по городу."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (city,))
    products = cur.fetchall()
    conn.close()
    return products


def get_products_low_stock():
    """Товары с количеством ≤ 6."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 6")
    products = cur.fetchall()
    conn.close()
    return products


def get_cities():
    """Список всех городов."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT страна FROM Товар ORDER BY страна")
    cities = [row[0] for row in cur.fetchall()]
    conn.close()
    return cities


def print_catalog(products):
    """Каталог с индикатором."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 60)

    for p in products:
        country = p[1]
        city = p[2]
        price = p[4]
        amount = p[5]

        indicator = "много" if amount > 6 else "мало"
        highlight = "⚠️" if amount <= 3 else "  "

        print(f"{highlight} {country} ({city})")
        print(f"   Цена: {price} руб. | Кол-во: {amount} ({indicator})")

    print("=" * 60)


if __name__ == "__main__":
    print("1. Все товары")
    print_catalog(get_all_products())

    print("\n2. Города:")
    for cat in get_cities():
        print(f"   - {cat}")

    print("\n3. Товары с низким остатком (≤6):")
    print_catalog(get_products_low_stock())