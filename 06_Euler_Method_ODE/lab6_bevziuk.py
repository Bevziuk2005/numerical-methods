import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Задача Коші
def f(x, y):
    denom = x**3 + y + 1
    if abs(denom) < 1e-14:
        raise ZeroDivisionError("У формулі виникло ділення на нуль або дуже мале число.")
    return 3 * x**2 / denom

# Метод Ейлера
def euler_method(x0, y0, b, eps):
    if b <= x0:
        raise ValueError("Кінець відрізка має бути більшим за початок.")
    n = max(1, math.ceil((b - x0) / eps))
    h = (b - x0) / n
    history = []
    x = x0
    y = y0
    for k in range(n + 1):
        history.append((k, x, y, f(x, y)))
        if k == n:
            break
        y = y + h * f(x, y)
        x = x + h
    return history, h

# Створння графіку
def draw_graph(history):
    ax.clear()
    xs = [row[1] for row in history]
    ys = [row[2] for row in history]
    ax.plot(xs, ys, marker="o", linewidth=2, label="Наближений розв’язок методом Ейлера")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Графік наближеного розв’язку")
    ax.grid(True, linestyle=":")
    ax.legend()
    canvas.draw()

# Заповнення таб
def fill_table(history):
    for item in table.get_children():
        table.delete(item)
    for k, x, y, slope in history:
        table.insert(
            "",
            tk.END,
            values=(
                k,
                f"{x:.6f}",
                f"{y:.6f}",
                f"{slope:.6f}"
            )
        )

# Розрахунок
def calculate():
    try:
        x0 = float(start_entry.get().replace(",", "."))
        b = float(end_entry.get().replace(",", "."))
        eps = float(eps_entry.get().replace(",", "."))

        if abs(x0 - 1.0) > 1e-12:
            raise ValueError("Для цієї задачі початкове значення x0 має бути 1, бо задано y(1)=0.")

        y0 = 0.0
        history, h = euler_method(x0, y0, b, eps)
        final_x = history[-1][1]
        final_y = history[-1][2]
        result_var.set(
            f"Метод Ейлера виконано успішно.\n"
            f"Початкова умова: y(1)=0\n"
            f"Сталий крок h = {h:.6f}\n"
            f"Кількість кроків = {len(history) - 1}\n"
            f"Останнє наближення: y({final_x:.6f}) = {final_y:.6f}"
        )
        fill_table(history)
        draw_graph(history)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

# GUI
root = tk.Tk()
root.title("Лабораторна робота №6 — Метод Ейлера")
root.geometry("1100x780")
root.minsize(1000, 700)
top = ttk.Frame(root, padding=10)
top.pack(fill=tk.X)
ttk.Label(
    top,
    text="Задача Коші: y' = 3x² / (x³ + y + 1),   y(1)=0",
    font=("Arial", 12, "bold")
).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 8))
ttk.Label(top, text="Початок відрізка x0:").grid(row=1, column=0, sticky="w")
start_entry = ttk.Entry(top, width=12)
start_entry.grid(row=1, column=1, sticky="w", padx=6)
start_entry.insert(0, "1")
ttk.Label(top, text="Кінець відрізка:").grid(row=1, column=2, sticky="w")
end_entry = ttk.Entry(top, width=12)
end_entry.grid(row=1, column=3, sticky="w", padx=6)
end_entry.insert(0, "2")
ttk.Label(top, text="Точність ε:").grid(row=1, column=4, sticky="w")
eps_entry = ttk.Entry(top, width=12)
eps_entry.grid(row=1, column=5, sticky="w", padx=6)
eps_entry.insert(0, "0.01")
btn_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
btn_frame.pack(fill=tk.X)
ttk.Button(btn_frame, text="Обчислити", command=calculate).pack(side=tk.LEFT, padx=5)
result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, justify="left", wraplength=1000)
result_label.pack(fill=tk.X, padx=10, pady=(0, 10))
# Графік
graph_frame = ttk.LabelFrame(root, text="Графік наближеного розв’язку", padding=10)
graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
fig, ax = plt.subplots(figsize=(7, 3))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, graph_frame)
toolbar.update()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
# Таблиця
table_frame = ttk.LabelFrame(root, text="Таблиця ітерацій", padding=10)
table_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))
columns = ("k", "x", "y", "f(x, y)")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
table.heading("k", text="k")
table.heading("x", text="x_k")
table.heading("y", text="y_k")
table.heading("f(x, y)", text="f(x_k, y_k)")
table.column("k", width=60, anchor="center")
table.column("x", width=160, anchor="center")
table.column("y", width=160, anchor="center")
table.column("f(x, y)", width=200, anchor="center")
table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()