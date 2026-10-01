"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_products_map():
    """Возвращает словарь {product_id: Product} для связи заказов с товарами."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар")
    rows = cur.fetchall()
    conn.close()

    products = {}
    for row in rows:
        p = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            price=row[4],
            quantity=row[5],
            duration=row[3]
        )
        products[p.id] = p
    return products


def get_all_orders():
    """Возвращает список объектов Order из БД."""
    products = get_all_products_map()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        # Предполагаемая структура таблицы Заказ:
        #   0: id, 1: дата, 2: клиент, 3: product_id, 4: quantity
        product_id = row[3]
        product = products.get(product_id)
        if product is None:
            print(f"⚠️ Товар с id={product_id} не найден, заказ №{row[0]} пропущен")
            continue

        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product,
            quantity=row[4]
        )
        orders.append(order)
    return orders


def print_orders(orders):
    """Выводит список заказов."""
    print(f"\n{'=' * 70}")
    print(f"ЗАКАЗЫ ({len(orders)})")
    print("=" * 70)

    for o in orders:
        mark = "  " if o.is_available() else "❌ "
        print(f"{mark}{o.info()}")

    print("=" * 70)


def total_orders_sum(orders):
    """Общая сумма всех заказов."""
    return sum(o.total() for o in orders)


if __name__ == "__main__":
    orders = get_all_orders()
    print_orders(orders)

    print(f"\nОбщая сумма заказов: {total_orders_sum(orders):.2f} руб.")