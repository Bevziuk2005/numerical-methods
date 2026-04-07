import tkinter as tk
from tkinter import messagebox, ttk
import math

# функції
def phi1(x, y):
    return math.exp(x) * math.cos(y) - 1
def phi2(x, y):
    return math.exp(x) * math.sin(y) + 1

# збіжність
def check_convergence(x, y):
    e = math.exp(x)

    dphi1_dx = e * math.cos(y)
    dphi1_dy = -e * math.sin(y)
    dphi2_dx = e * math.sin(y)
    dphi2_dy = e * math.cos(y)

    q1 = abs(dphi1_dx) + abs(dphi1_dy)
    q2 = abs(dphi2_dx) + abs(dphi2_dy)
    return max(q1, q2)

# метод Простої Ітерації
def simple_iteration(x0, y0, eps, max_iter=100):
    x, y = x0, y0
    history = [(x, y)]

    for _ in range(max_iter):
        x_new = phi1(x, y)
        y_new = phi2(x, y)
        history.append((x_new, y_new))

        if max(abs(x_new - x), abs(y_new - y)) < eps:
            return x_new, y_new, history
        x, y = x_new, y_new
    return x, y, history

# графік
def draw_graph(history):
    canvas.delete("all")
    width = 500
    height = 300
    margin = 40

    xs = [p[0] for p in history]
    ys = [p[1] for p in history]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    if max_x - min_x == 0:
        max_x += 1
    if max_y - min_y == 0:
        max_y += 1

    def scale_x(x):
        return margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)
    def scale_y(y):
        return height - (margin + (y - min_y) / (max_y - min_y) * (height - 2 * margin))

    canvas.create_line(margin, height - margin, width - margin, height - margin, width=2)
    canvas.create_line(margin, margin, margin, height - margin, width=2)
    canvas.create_text(width / 2, height - 10, text="x")
    canvas.create_text(10, height / 2, text="y", angle=90)

    for i in range(len(xs) - 1):
        x1, y1 = scale_x(xs[i]), scale_y(ys[i])
        x2, y2 = scale_x(xs[i + 1]), scale_y(ys[i + 1])
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="red")
        canvas.create_text(x1, y1 - 10, text=str(i), font=("Arial", 7))

    x_last, y_last = scale_x(xs[-1]), scale_y(ys[-1])
    canvas.create_oval(x_last - 5, y_last - 5, x_last + 5, y_last + 5, fill="green")

# таблиця ітерацій
def fill_table(history):
    for row in table.get_children():
        table.delete(row)
    for i, (x, y) in enumerate(history):
        table.insert("", "end", values=(i, f"{x:.5f}", f"{y:.5f}"))

# функція підрахунку
def solve():
    try:
        def parse(e):
            return float(e.get().replace(",", "."))

        x0 = parse(x_entry)
        y0 = parse(y_entry)
        eps = parse(eps_entry)
        q = check_convergence(x0, y0)

        if q < 1:
            convergence_text = (
                f"{q:.4f} < 1 → метод збігається\n"
            )
        else:
            messagebox.showerror(
                "Помилка",
                f"q = {q:.4f} ≥ 1\nМетод може не збігатися"
            )
            return

        x, y, history = simple_iteration(x0, y0, eps)
        result_var.set(
            convergence_text +
            f"Результат:\n"
            f"x = {x:.5f}\n"
            f"y = {y:.5f}"
        )
        draw_graph(history)
        fill_table(history)

    except Exception as e:
        messagebox.showerror("Помилка", str(e))

# GUI
root = tk.Tk()
root.title("Метод простої ітерації")
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Початкова точка").grid(row=0, column=0, columnspan=2)
tk.Label(frame, text="x").grid(row=1, column=0)
tk.Label(frame, text="y").grid(row=1, column=1)

x_entry = tk.Entry(frame, width=10)
y_entry = tk.Entry(frame, width=10)
x_entry.grid(row=2, column=0)
y_entry.grid(row=2, column=1)

x_entry.insert(0, "-0.9")
y_entry.insert(0, "1.4")

tk.Label(root, text="Точність ε").pack()
eps_entry = tk.Entry(root, width=10)
eps_entry.insert(0, "0.0001")
eps_entry.pack()

tk.Button(root, text="Розв'язати", command=solve).pack(pady=10)
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Arial", 11), justify="left").pack()

canvas = tk.Canvas(root, width=500, height=300, bg="white")
canvas.pack(pady=10)
columns = ("k", "x", "y")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)

for c in columns:
    table.heading(c, text=c)
    table.column(c, width=100, anchor="center")

table.pack()
root.mainloop()