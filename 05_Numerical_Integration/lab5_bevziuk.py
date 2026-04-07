import tkinter as tk
from tkinter import messagebox
import math

# підінтегральна функція
def f(x):
    return 1 / math.sqrt(2 * x**2 + 1)
# межі інтегрування
a = 0.8
b = 1.6

# Метод лівих прямокутників
def left_rectangles(h):
    n = int((b - a) / h)
    s = 0
    for i in range(n):
        x = a + i * h
        s += f(x)
    I = h * s
    return I, n

# Метод трапецій
def trapezoid(n):
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s += f(a + i * h)
    return h * s

# Метод подвійних перерахунків
def trapezoid_precision(eps):
    n = 2
    I1 = trapezoid(n)
    while True:
        n = n * 2
        I2 = trapezoid(n)
        error_estimate = abs(I2 - I1) / 3
        if error_estimate < eps:
            return I2, n, error_estimate
        I1 = I2

# Розрахунки
def calculate():
    try:
        h = float(entry_h.get())
        eps = float(entry_eps.get())

        left_result, n_left = left_rectangles(h)
        trap_result, n_trap, error_estimate = trapezoid_precision(eps)

        result_text.set(
            f"Метод лівих прямокутників\n"
            f"Кількість розбиттів = {n_left}\n"
            f"Значення інтеграла ≈ {left_result:.6f}\n\n"

            f"Метод трапецій (метод подвійних перерахунків)\n"
            f"Кількість розбиттів = {n_trap}\n"
            f"Значення інтеграла ≈ {trap_result:.6f}\n"
            f"Оцінка похибки ≈ {error_estimate:.6f}"
        )
    except:
        messagebox.showerror("Помилка", "Перевірте введені дані")

# GUI
root = tk.Tk()
root.title("Чисельне обчислення визначеного інтеграла")
frame = tk.Frame(root)
frame.pack(pady=10)
tk.Label(frame, text="Крок h для методу лівих прямокутників:").grid(row=0, column=0)
entry_h = tk.Entry(frame)
entry_h.insert(0, "0.01")
entry_h.grid(row=0, column=1)
tk.Label(frame, text="Точність ε для методу трапецій:").grid(row=1, column=0)
entry_eps = tk.Entry(frame)
entry_eps.insert(0, "0.001")
entry_eps.grid(row=1, column=1)
tk.Button(frame, text="Обчислити", command=calculate).grid(row=2, column=0, columnspan=2, pady=5)
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left").pack(pady=10)
root.mainloop()