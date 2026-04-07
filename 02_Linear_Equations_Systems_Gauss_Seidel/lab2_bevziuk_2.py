import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

# Перевірка діагонального переваження
def is_diagonally_dominant(A):
    for i in range(3):
        diag = abs(A[i][i])
        others = sum(abs(A[i][j]) for j in range(3) if j != i)
        if diag <= others:
            return False
    return True

# Метод Зейделя
def gauss_seidel(A, b, eps=0.001, max_iter=100):
    x = np.zeros(3)
    history = [x.copy()]
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(3):
            s1 = sum(A[i][j]*x_new[j] for j in range(i))
            s2 = sum(A[i][j]*x[j] for j in range(i+1,3))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        history.append(x_new.copy())
        if np.linalg.norm(x_new-x,ord=np.inf) < eps:
            return x_new, history
        x = x_new
    return x, history

# Малювання траєкторії
def draw_graphs(history):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    pairs = [("x1","x2"),("x1","x3"),("x2","x3")]
    colors = ["blue","green","purple"]

    for idx, (i,j) in enumerate([(0,1),(0,2),(1,2)]):
        c = tk.Canvas(graph_frame,width=300,height=250,bg="white",highlightthickness=1,highlightbackground="black")
        c.grid(row=0,column=idx,padx=10)

        xs = [h[i] for h in history]
        ys = [h[j] for h in history]

        min_x,max_x = min(xs),max(xs)
        min_y,max_y = min(ys),max(ys)

        if max_x-min_x==0: max_x+=1
        if max_y-min_y==0: max_y+=1

        def scale_x(x): return 30 + (x-min_x)/(max_x-min_x)*(240)
        def scale_y(y): return 220 - (y-min_y)/(max_y-min_y)*(180)

        c.create_line(30,220,270,220,width=2)
        c.create_line(30,40,30,220,width=2)
        c.create_text(150,230,text=pairs[idx][0])
        c.create_text(10,130,text=pairs[idx][1],angle=90)

        for k in range(len(xs)-1):
            x1,y1 = scale_x(xs[k]),scale_y(ys[k])
            x2,y2 = scale_x(xs[k+1]),scale_y(ys[k+1])
            c.create_line(x1,y1,x2,y2,fill=colors[idx],width=2)
            c.create_oval(x1-3,y1-3,x1+3,y1+3,fill="red")
            c.create_text(x1-5,y1-10,text=str(k),font=("Arial",7))

        x_last,y_last = scale_x(xs[-1]),scale_y(ys[-1])
        c.create_oval(x_last-4,y_last-4,x_last+4,y_last+4,fill="green")
        c.create_text(x_last-5,y_last-10,text=str(len(xs)-1),font=("Arial",7))

# Заповнення таблиці ітерацій
def fill_table(history):
    for row in table.get_children():
        table.delete(row)
    for i,h in enumerate(history):
        table.insert(
            "",
            "end",
            values=(
                i,
                f"{h[0]:.5f}",
                f"{h[1]:.5f}",
                f"{h[2]:.5f}"
            )
        )

# Розв'язання
def solve():
    try:
        def parse(e):
            return float(e.get().replace(",", "."))

        A = np.array([
            [parse(a11),parse(a12),parse(a13)],
            [parse(a21),parse(a22),parse(a23)],
            [parse(a31),parse(a32),parse(a33)]
        ])

        b = np.array([
            parse(b1),
            parse(b2),
            parse(b3)
        ])

        eps = parse(eps_entry)

        if not is_diagonally_dominant(A):
            messagebox.showerror(
                "Помилка",
                "Матриця не має діагонального переваження.\n"
                "Метод Зейделя може не збігатися."
            )
            return
        solution,history = gauss_seidel(A,b,eps)

        result_var.set(
            f"x1 = {solution[0]:.5f}\n"
            f"x2 = {solution[1]:.5f}\n"
            f"x3 = {solution[2]:.5f}"
        )
        draw_graphs(history)
        fill_table(history)

    except Exception as e:
        messagebox.showerror("Помилка",str(e))


# GUI
root = tk.Tk()
root.title("Метод Зейделя")

top = tk.Frame(root)
top.pack(pady=10)

tk.Label(top,text="Вводьте числа через крапку (.)").grid(row=0,column=0,columnspan=4)

tk.Label(top,text="x1").grid(row=1,column=0)
tk.Label(top,text="x2").grid(row=1,column=1)
tk.Label(top,text="x3").grid(row=1,column=2)
tk.Label(top,text="b").grid(row=1,column=3)

def entry(r,c):
    e=tk.Entry(top,width=7)
    e.grid(row=r,column=c,padx=3,pady=3)
    return e

a11=entry(2,0)
a12=entry(2,1)
a13=entry(2,2)
b1=entry(2,3)
a21=entry(3,0)
a22=entry(3,1)
a23=entry(3,2)
b2=entry(3,3)
a31=entry(4,0)
a32=entry(4,1)
a33=entry(4,2)
b3=entry(4,3)

tk.Label(root,text="Точність ε").pack()

eps_entry=tk.Entry(root,width=10)
eps_entry.insert(0,"0.001")
eps_entry.pack()

tk.Button(
    root,
    text="Розв'язати",
    command=solve,
    height=2
).pack(pady=10)

result_var=tk.StringVar()

tk.Label(
    root,
    textvariable=result_var,
    font=("Arial",12)
).pack()

# графік
graph_frame = tk.Frame(root)
graph_frame.pack(pady=10)


# Таблиця ітерацій
columns=("k","x1","x2","x3")
table=ttk.Treeview(root,columns=columns,show="headings",height=8)

for c in columns:
    table.heading(c,text=c)
    table.column(c,width=100,anchor="center")

table.pack(pady=10)

root.mainloop()