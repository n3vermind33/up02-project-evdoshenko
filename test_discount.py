"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""

    test_cases = [
        # (id, цена, дата расчёта, ожидание, пояснение)

        (1, 50000, datetime(2026, 10, 15), 50000,
         "Тур 1 — есть брони в сентябре"),

        (2, 150000, datetime(2026, 10, 15), 150000,
         "Тур 2 — есть бронь"),

        (3, 120000, datetime(2026, 10, 15), 120000,
         "Тур 3 — есть брони"),

        (4, 75000, datetime(2026, 10, 15), 67500,
         "Тур 4 — нет броней → 10% скидка"),

        (5, 100000, datetime(2026, 10, 15), 90000,
         "Тур 5 — нет броней → 10% скидка"),

        (2, 60000, datetime(2026, 11, 15), 54000,
         "В октябре заказов нет → 10% скидка"),

        (1, 50000, datetime(2026, 11, 15), 45000, 
         "Нет заказов → 10% скидка"),

        (4, 90000, datetime(2026, 9, 1), 81000,
         "Август — заказов нет"),

        (1, 50000, datetime(2026, 10, 1), 50000,
         "Дата расчёта 1 октября → проверяется сентябрь"),

        (1, 50000, datetime(2026, 10, 31), 50000,
         "Дата расчёта 31 октября → проверяется сентябрь"),

        (4, 0, datetime(2026, 10, 15), 0,
         "Товар с нулевой ценой"),

        (1, 50000, datetime(2026, 11, 15), 45000,
         "Заказ был в сентябре, но не в октябре → 10% скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed = 0

    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(
            product_id,
            price,
            date
        )

        status = "✅" if result == expected else "❌"

        if result == expected:
            passed += 1

        print(
            f"{status} Тур {product_id}: {price} → {result} "
            f"(ожидалось {expected}) — {comment}"
        )

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()
try:
    calculate_price_with_discount(
        4, 90000, datetime(2026, 10, 15), -1
    )
    print("❌ Отрицательное количество не вызвало ошибку")
except ValueError:
    print("✅ Отрицательное количество → ошибка")