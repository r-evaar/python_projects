from tkinter import *
from tkinter import ttk

PAD_X = 20
PAD_Y = 20

root = Tk()
style = ttk.Style(root)

root.title("Positioning")
root.minsize(height=400, width=600)
root.config(padx=PAD_X, pady=PAD_Y)

example = Label(text="*Example Label at (400,0)\n(excluding padding)")
example.place(x=400, y=0)

title = Label(text="Main Title", font=("Bahnschrift", 16, "bold"))
title.place(x=300-PAD_X, y=20-PAD_Y, anchor='n')

example_2 = Label(text="Adaptive-Position")
example_2.place(relx=0.5, rely=0.5, anchor='center')

example_3 = Label(text="Static-Position")
example_3.place(x=300-PAD_X, y=150-PAD_Y, anchor='center')

btns = []
for i in range(3):
    btns += [ttk.Button(text=f"Grid: ({i},{i})")]
    btns[i].grid(column=i, row=i)

# Using @pack and @grid in the same interface results in an error

padded_btn = ttk.Button(text="Padded Btn", padding=(20, 20))
padded_btn.grid(column=0, row=3)

padded_label = Label(text="Padded Label")
padded_label.config(padx=20, pady=20)
padded_label.grid(column=0, row=4)

mainloop()
