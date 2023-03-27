import tkinter as tk
from tkinter import ttk

W, H = [600, 100]
FONT = ("Bahnschrift", 16, "bold")
FONT_V = ("Bahnschrift", 12, "normal")

root = tk.Tk()
style = ttk.Style(root)

root.title("Mile-Km Converter")
root.minsize(W, H); root.maxsize(W, H)

symbol_data = tk.PhotoImage(file='./arrows.png').subsample(4)
symbol_placer = tk.Label(image=symbol_data)
symbol_placer.place(relx=0.49, rely=0.5, anchor='center')

# Function to validate input
def validate_input(new_value):
    if new_value == "":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False

validate_cmd = root.register(validate_input)

km_lbl = ttk.Label(text='Km', font=FONT)
km_val = ttk.Entry(width=10, font=FONT_V, validate="key", validatecommand=(validate_cmd, '%P'))
mi_lbl = ttk.Label(text='Mile', font=FONT)
mi_val = ttk.Entry(width=10, font=FONT_V, validate="key", validatecommand=(validate_cmd, '%P'))

km_val.place(relx=0.1, rely=0.5, anchor='w')
km_lbl.place(relx=0.33, rely=0.5, anchor='w')
mi_val.place(relx=0.6, rely=0.5, anchor='w')
mi_lbl.place(relx=0.9, rely=0.5, anchor='e')


def update_km(_):
    km_val.delete(0, tk.END)
    val = mi_val.get()
    if val != '': km_val.insert(0, f"{float(val) * 1.609344:.5f}")

def update_mi(_):
    mi_val.delete(0, tk.END)
    val = km_val.get()
    if val != '': mi_val.insert(0, f"{float(val) / 1.609344:.5f}")

mi_val.bind("<KeyRelease>", update_km)
km_val.bind("<KeyRelease>", update_mi)

root.mainloop()
