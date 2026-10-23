"""Проверка вывода полей."""
from dataclasses import fields, is_dataclass
import databases as db
from db_products import get_all_products   # ← функция живёт здесь


def test_fields():
    """Проверяет, что все поля на месте."""
    products = get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 6   # минимум полей для макета
    errors = 0

    for p in products:
        # Способ 1: если Product — dataclass
        if is_dataclass(p):
            names = [f.name for f in fields(p)]
            count = len(names)
        else:
            # Способ 2: обычный класс — считаем атрибуты экземпляра
            names = [k for k in vars(p) if not k.startswith("_")]
            count = len(names)

        if count < required_count:
            print(f"❌ Товар id={p.product_id}: мало полей ({count}) — {names}")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()