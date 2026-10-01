"""Алгоритм расчёта цены со скидкой 10%."""
import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH

DISCOUNT_PERCENT = 10


def _columns(table):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cur.fetchall()]
    conn.close()
    return cols


def _find_column(table, candidates):
    cols = _columns(table)
    for name in candidates:
        if name in cols:
            return name
    raise RuntimeError(f"Нет столбца из {candidates} в {table}. Есть: {cols}")


def get_previous_month_range(date):
    first_of_current = date.replace(day=1)
    last_of_previous = first_of_current - timedelta(days=1)
    first_of_previous = last_of_previous.replace(day=1)
    return (
        first_of_previous.strftime("%Y-%m-%d"),
        last_of_previous.strftime("%Y-%m-%d"),
    )


def has_orders_in_period(product_id, start_date, end_date):
    product_col = _find_column(
        "Заказ", ["товар_id", "product_id", "id_товара", "товар", "product", "id_товар"]
    )
    date_col = _find_column(
        "Заказ", ["дата", "date", "дата_заказа", "order_date"]
    )

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT {date_col} FROM Заказ WHERE {product_col} = ?", (product_id,))
    rows = cur.fetchall()
    conn.close()

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    for (raw,) in rows:
        if raw is None:
            continue
        if isinstance(raw, str):
            parsed = None
            for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d", "%d/%m/%Y"):
                try:
                    parsed = datetime.strptime(raw, fmt).date()
                    break
                except ValueError:
                    continue
            if parsed is None:
                continue
        else:
            parsed = raw
        if start <= parsed <= end:
            return True
    return False


def calculate_price_with_discount(product_id, price, date):
    price = float(price)
    start, end = get_previous_month_range(date)
    if has_orders_in_period(product_id, start, end):
        return price
    return price * (1 - DISCOUNT_PERCENT / 100)