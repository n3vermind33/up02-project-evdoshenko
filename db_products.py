"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product

IMAGE_DIR = "/resources"

def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6]
        )
        products.append(product)
    return products


def get_products_by_duration(duration):
    """Возвращает товары с указанной длительностью поездки."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE длительность = ?", (duration,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6]
        )
        products.append(product)
    return products


def get_all_durations():
    """Возвращает список уникальных значений длительности из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT длительность FROM Товар ORDER BY длительность")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6]
        )
        products.append(product)
    return products


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if int(p.quantity) <= 3 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


def total_price_all(products):
    """Считает общую стоимость всех товаров (цена × количество)."""
    total = 0
    for p in products:
        total += float(p.price) * int(p.quantity)
    return total


if __name__ == "__main__":
    all_products = get_all_products()

    print("1. Все товары:")
    print_catalog_with_highlight(all_products)

    print("\n2. Товары с одинаковой длительностью:")
    durations = get_all_durations()
    print(f"Доступные варианты длительности: {durations}")

    for d in durations:
        print(f"\n--- Длительность: {d} ---")
        print_catalog_with_highlight(get_products_by_duration(d))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())

    print(f"\n4. Общая стоимость всех товаров: {total_price_all(all_products):.2f} руб.")