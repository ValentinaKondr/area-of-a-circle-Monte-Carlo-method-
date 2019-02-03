import tkinter
from tkinter import messagebox
import random
import math

MAX_HEIGHT = 650
MIDDLE_LINE = MAX_HEIGHT // 2
CANVAS_SIZE = 620
RECT_SIZE = 600
H_RECT_SIZE = RECT_SIZE // 2
CORRECTION = (CANVAS_SIZE - RECT_SIZE) // 2

def show(dir):
    root = tkinter.Tk()
    root.geometry("500x400")
    root.resizable(0, 0)
    root.title("Координаты точек")
    coord_listbox = tkinter.Listbox(root, width=25, height=22)
    coord_listbox.grid(row=0, column=0, columnspan=3, rowspan=2, sticky=tkinter.W + tkinter.E, padx=5, pady=5)
    for key in dir:
        color = "light slate gray" if dir[key][2] else "indian red"
        coord = "({0:.4f};{1:.3f})".format(dir[key][0], dir[key][1])
        coord_listbox.insert(tkinter.END, coord)
        coord_listbox.itemconfig(int(key), {'bg': color})
    l  = tkinter.Label(root, text="В списке слева представлены\n"
                                  "координаты точек. Фон указывает,\n"
                                  "попадает ли она в пределы\n"
                                  "окружности.\n"
                                  "Красный фон - нет\n"
                                  "Серый - да")
    l.grid(row=0, column=4, rowspan=2)
    tkinter.Button(root, text="Закрыть", command=root.withdraw).grid(row=1, column=4)


def create_win(str, dir):
    root = tkinter.Tk()
    root.resizable(0, 0)
    root.geometry("400x130")
    root.title("Результаты")
    root.resizable(0, 0)
    #print(dir)
    tkinter.Label(root, text=str, font="Helvetica 14").pack()
    tkinter.Button(root, text="Показать точки", command=lambda : show(dir)).pack()
    tkinter.Button(root, text="Закрыть", command=root.withdraw).pack()


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle_arc = _create_circle_arc

def draw_dot(x, y):
    start_x = -4
    start_y =  7
    step = RECT_SIZE // 10
    new_x = (x - start_x) * step + CORRECTION
    new_y = (y - start_y) * step - CORRECTION
    canvas.create_oval(new_x - 1, - new_y - 1, new_x + 1, - new_y + 1, fill="FIREBRICK1", tag="sad", outline="firebrick2")

def create_dots(num):
    canvas.delete("sad")
    m = 0
    d = dict()
    for i in range(num):
        xr = random.random() * 10 - 4
        yr = random.random() * 10 - 3
        in_area = ((xr - 1)**2 + (yr - 2)**2 <= 25)
        d[i] = [xr, yr, in_area]
        m += int(in_area)
#        print("Случайная точка ({0:3.4f}; {1:3.4f})".format(xr, yr))
        draw_dot(xr, yr)
    try:
        S = (m/num) * 100
    except:
        S = 0
    real_square = math.pi * 5**2
    error_abs = math.fabs(real_square - S)
    error_otn = (error_abs/real_square)*100
    str = "Площадь круга, исходя из выборки: {0}\nРеальная площадь круга: {1:.4f}\n" \
          "Абсолютная погрешность: ±{2:.4f}\nОтносительная погрешность: {3:.2f}%".format(S, real_square, error_abs, error_otn)
    create_win(str, d)
    #print("Площадь круга, исходя из выборки: {0}".format(S))
    #print("Реальная площадь круга: {0:.4f}".format(math.pi * 5**2))

def draw():
    x0 = 1
    y0 = 2
    middle = (CANVAS_SIZE - 20) // 2 + CORRECTION
    step = (CANVAS_SIZE - 20) // 10
    canvas.create_line(middle, 0, middle, MAX_HEIGHT + CORRECTION)
    canvas.create_line(0, middle, MAX_HEIGHT + CORRECTION, middle)
    for i in range(0, 6):
        canvas.create_line(middle - i*step, 0, middle - i*step, MAX_HEIGHT)
        canvas.create_text((middle - i * step) - 10, middle + 2*step - 10, text= x0 - i)
        canvas.create_text((middle + (i + 1) * step) - 10, middle + 2*step - 10, text= x0 + i + 1)
        canvas.create_text(middle - step - 10, (middle - i* step) - 10, text= y0 + i)
        canvas.create_text(middle - step - 10, (middle + (i + 1) * step ) - 10, text=y0 - i - 1)
        canvas.create_line(middle + i * step, 0, middle + i * step, MAX_HEIGHT)
        canvas.create_line(0, middle + i * step, MAX_HEIGHT, middle + i * step)
        canvas.create_line(0, middle - i * step, MAX_HEIGHT, middle - i * step)
    canvas.create_line(middle - step, 0, middle - step, MAX_HEIGHT, width=2)
    canvas.create_line(0, middle + 2*step, MAX_HEIGHT, middle + 2*step, width=2)

def fetch():
    num = e.get()
    if not num.isnumeric():
        messagebox.showerror("Ошибка ввода", "Вы ввели неправильное значение")
    elif int(num) <= 0:
        messagebox.showerror("Ошибка ввода", "Количество точек не может быть отрицательным или равняться нулю")
    else:
        create_dots(int(num))

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, borderwidth=0, highlightthickness=0, bg="ghost white")
canvas.grid(row=0, columnspan=3)
canvas.create_rectangle(CORRECTION, CORRECTION, RECT_SIZE + CORRECTION, RECT_SIZE + CORRECTION, fill="LemonChiffon2", outline="white")
tkinter.Button(root, text="Применить", command=fetch, width=20, height=3, font="helvetica 14", fg="dark slate gray").grid(row=1, column=1, rowspan=2)
tkinter.Button(root, text="Закрыть", command=quit, width=20, height=3, font="helvetica 14", fg="dark slate gray").grid(row=1, column=2, rowspan=2)

tkinter.Label(root, text="Введите количество точек: ", font="helvetica 14").grid(row=1, column=0)
e = tkinter.Entry(root, bg="white smoke", fg="dark slate gray", width=30)
e.grid(row=2, column=0)
canvas.create_circle(H_RECT_SIZE + CORRECTION, H_RECT_SIZE + CORRECTION, 300, fill="khaki", outline="dark goldenrod", width=1)
draw()
root.wm_title("Визуализация равномерного распределения")
root.resizable(0, 0)
root.mainloop()
