import math

# -------- Захардкоджена функція --------
def f(x):
    return x - math.sin(x) - 0.25


# 1. Метод половинного ділення (дихотомії)
def bisection_method(func, a, b, eps):
    iteration = 0  # лічильник
    x_values = []      # список наближень x
    fx_values = []     # список значень f(x)

    while True:
        iteration += 1

        c = (a + b) / 2
        # Збереження значень у списки
        x_values.append(c)
        fx_values.append(func(c))

        # перевірка умови виходу
        if abs(func(c)) < eps:
            break

        # зміна відрізку через перевірку зміни знаку
        if func(a) * func(c) < 0:
            b = c   #корінь в [a, c]
        else:
            a = c   #корінь в [с, b]

    # відповідь
    root = (a + b) / 2
    return root, iteration, x_values, fx_values


# 2. Метод хорд
def chord_method(func, a, b, eps):
    iteration = 0  # лічильник
    x_values = []      # список наближень x
    fx_values = []     # список значень f(x)
    c_prev = None   # попереднє с, для умови виходу

    while True:
        iteration += 1

        c = a - (func(a) / (func(b) - func(a))) * (b - a)
        x_values.append(c)
        fx_values.append(func(c))

        # умова виходу від 2+ ітерації
        if c_prev is not None:
            if abs(c - c_prev) < eps:
                break

        if func(a) * func(c) < 0:
            b = c
        else:
            a = c
        c_prev = c

    root = c
    return root, iteration, x_values, fx_values


if __name__ == "__main__":

    # Задані параметри
    a = -50
    b = 20
    eps = 0.001

    print("Розв'язання рівняння x - sin(x) = 0.25")
    print("Інтервал:", a, b)
    print("Точність:", eps)
    print()

    # --- Метод половинного ділення ---
    root_bis, iter_bis, x_bis, fx_bis = bisection_method(f, a, b, eps)

    print("Метод половинного ділення")
    print("Кількість ітерацій:", iter_bis)
    print("Корінь:", root_bis)
    print("Список x:", x_bis)
    print("Список f(x):", fx_bis)
    print()
    print("-" * 50)
    print()

    # --- Метод хорд ---
    root_chord, iter_chord, x_chord, fx_chord = chord_method(f, a, b, eps)

    print("Метод хорд")
    print("Кількість ітерацій:", iter_chord)
    print("Корінь:", root_chord)
    print("Список x:", x_chord)
    print("Список f(x):", fx_chord)
