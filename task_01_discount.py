price = float(input("Введите цену: "))

discount = 25
final_price = price * (1 - discount / 100)

print(f"Цена со скидкой: {final_price:.2f} руб.")