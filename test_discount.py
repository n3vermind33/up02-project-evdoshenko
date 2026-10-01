"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount

def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)

    test_cases = [
        (1, 50000,  50000,  "Тур 1 — есть брони в сентябре"),
        (2, 150000, 150000, "Тур 2 - есть бронь"),
        (3, 120000, 120000, "Тур 3 — есть брони"),
        (4, 75000,  67500,  "Тур 4 — нет броней → 10% скидка"),
        (5, 100000, 90000,  "Тур 5 — нет броней → 10% скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Тур {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()