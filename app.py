import random
from tkinter import *
from tkinter import ttk

import numpy as np

from cell import Cell


x_size = None
y_size = None
grid = None
begin_id = None


def draw_grid():
    canvas.delete('all')
    global x_size
    global y_size
    square = 10
    for i in range(y_size):
        for j in range(x_size):
            x, y = grid[i][j].position_in_canvas
            canvas.create_rectangle(x, y, x + square, y + square, fill="white")


def build_grid():
    global x_size
    global y_size
    global grid
    x_size = int(x_size_ent.get())
    y_size = int(y_size_ent.get())
    grid = np.array([[Cell(i, j) for j in range(x_size)] for i in range(y_size)], dtype=object)
    draw_grid()


def draw_cells():
    global x_size
    global y_size
    square = 10
    for i in range(y_size):
        for j in range(x_size):
            x, y = grid[i][j].position_in_canvas
            if grid[i][j].next_state != grid[i][j].is_alive:
                if grid[i][j].next_state:
                    canvas.create_rectangle(x, y, x + square, y + square, fill="green")
                else:
                    canvas.create_rectangle(x, y, x + square, y + square, fill="white")
                grid[i][j].switch_state()


def calculate_state(cell):
    num_alive = 0
    x, y = cell.position_in_matrix
    for i in (x - 1, x, x + 1):
        for j in (y - 1, y, y + 1):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if grid[i][j].is_alive:
                    num_alive += 1
            except IndexError:
                pass
    if cell.is_alive:
        return not (num_alive == 2 or num_alive == 3)
    else:
        return num_alive == 3


def change_states_in_grid():
    global x_size
    global y_size
    for i in range(y_size):
        for j in range(x_size):
            if calculate_state(grid[i][j]):
                grid[i][j].next_state = not grid[i][j].is_alive
            else:
                grid[i][j].next_state = grid[i][j].is_alive


def start():
    change_states_in_grid()
    draw_cells()
    global begin_id
    begin_id = canvas.after(200, start)


def stop():
    canvas.after_cancel(begin_id)


def clean_cells():
    global x_size
    global y_size
    square = 10
    for i in range(y_size):
        for j in range(x_size):
            x, y = grid[i][j].position_in_canvas
            grid[i][j].is_alive = False
            canvas.create_rectangle(x, y, x + square, y + square, fill="white")


def prepare_to_draw_structure():
    global x_size
    global y_size
    clean_cells()
    x_grid_center = int(x_size / 2)
    y_grid_center = int(y_size / 2)
    return x_grid_center, y_grid_center


def draw_structure(structure):
    square = 10
    for struct in structure:
        x_struct, y_struct = struct
        grid[y_struct][x_struct].is_alive = True
        x, y = grid[y_struct][x_struct].position_in_canvas
        canvas.create_rectangle(x, y, x + square, y + square, fill="green")


def invariable():
    x_grid_center, y_grid_center = prepare_to_draw_structure()
    invariable_struct = ((x_grid_center, y_grid_center),
                         (x_grid_center + 1, y_grid_center),
                         (x_grid_center - 1, y_grid_center + 1),
                         (x_grid_center + 2, y_grid_center + 1),
                         (x_grid_center, y_grid_center + 2),
                         (x_grid_center + 1, y_grid_center + 2))
    draw_structure(invariable_struct)


def glider():
    x_grid_center, y_grid_center = prepare_to_draw_structure()
    glider_struct = ((x_grid_center, y_grid_center),
                     (x_grid_center + 1, y_grid_center),
                     (x_grid_center - 1, y_grid_center + 1),
                     (x_grid_center, y_grid_center + 1),
                     (x_grid_center + 1, y_grid_center + 2))
    draw_structure(glider_struct)


def oscillator():
    x_grid_center, y_grid_center = prepare_to_draw_structure()
    oscillator_struct = ((x_grid_center, y_grid_center),
                        (x_grid_center, y_grid_center + 1),
                        (x_grid_center, y_grid_center + 2))
    draw_structure(oscillator_struct)


def rand():
    x_grid_center, y_grid_center = prepare_to_draw_structure()
    random_stuct = []
    for i in range(x_grid_center * y_grid_center):
        x_struct = random.randint(0, x_grid_center * 2 - 1)
        y_struct = random.randint(0, y_grid_center * 2 - 1)
        random_stuct.append((x_struct, y_struct))
    draw_structure(random_stuct)


def structure_handler(event):
    values = ["Invariable", "Glider", "Oscillator", "Random"]
    current = structure_combo.current()
    value = values[current]
    func_map = {
        "Invariable": invariable,
        "Glider": glider,
        "Oscillator": oscillator,
        "Random": rand
    }
    func = func_map.get(value)
    func()


# GUI
root = Tk(className=" Cellular Automata 2D - The Game of Live")
root.minsize(800, 630)

frame = Frame(root)
frame.pack()

canvas = Canvas(frame, width=800, height=600)
canvas.pack(side=BOTTOM)

start_butt = Button(frame, text="Start", fg="white", bg="#263D42", width=10, command=start)
start_butt.pack(side=LEFT)

stop_butt = Button(frame, text="Stop", fg="white", bg="#263D42", width=10, command=stop)
stop_butt.pack(side=LEFT)

size_lab = Label(frame, text="Size (x,y): (")
size_lab.pack(side=LEFT)
default_x_size = IntVar(value=79)
x_size_ent = Entry(frame, width=4, textvariable=default_x_size)
x_size_ent.pack(side=LEFT)
colon_lab = Label(frame, text=",")
colon_lab.pack(side=LEFT)
default_y_size = IntVar(value=59)
y_size_ent = Entry(frame, width=4, textvariable=default_y_size)
y_size_ent.pack(side=LEFT)
bracket_lab = Label(frame, text=") ")
bracket_lab.pack(side=LEFT)
size_butt = Button(frame, text="Change size", fg="white", bg="#263D42", width=15, command=build_grid)
size_butt.pack(side=LEFT)

condition_lab = Label(frame, text="Condition: ")
condition_lab.pack(side=LEFT)
cond = StringVar(value="Constant")
condition_combo = ttk.Combobox(frame, width=10, values=["Constant"], textvariable=cond)
condition_combo.pack(side=LEFT)

structure_lab = Label(frame, text="Structure: ")
structure_lab.pack(side=LEFT)
structure_combo = ttk.Combobox(frame, width=15, value=["Invariable", "Glider", "Oscillator", "Random"])
structure_combo.pack(side=LEFT)
structure_combo.bind('<<ComboboxSelected>>', structure_handler)

build_grid()
root.mainloop()
