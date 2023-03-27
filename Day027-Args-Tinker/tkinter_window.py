import tkinter as tk
from tkinter import ttk
from copy import deepcopy  # tkiner objects can NOT be deep-copied

window = tk.Tk()
style = ttk.Style()
style.theme_use(themename='xpnative')

window.title("My First Python GUI")
window.minsize(height=480, width=720)

my_label = tk.Label(  # Create label object
    text="I'm A Label",
    font=("Bahnschrift", 16, "bold")
)
my_label.pack()  # Render the label on window (by default: top center)

[tk.Label(text=loc.capitalize()).pack(side=loc) for loc in ['left', 'right', 'bottom']]

my_label["text"] = "New Label"
my_label.config(text="Another Label")

def btn_callback(): my_label["text"] = "Button got clicked"
btn = ttk.Button(
    text="Click Me",
    command=btn_callback
)
btn.pack()

def inpt_value_changed(event): my_label["text"] = event.widget.get()
inpt = ttk.Entry(
    width=50,
)
inpt.pack()
inpt.bind("<KeyRelease>", inpt_value_changed)

def btn2_callback(): my_label["text"] = inpt.get()
btn2 = ttk.Button(text="Update", command=btn2_callback)
btn2.pack()

class btn3_callback_functor:
    def __init__(self, btn):
        self.forget = False
        self.btn = btn
    def __call__(self):
        self.forget = not self.forget
        self.btn.pack_forget() if self.forget else self.btn.pack()

btn3 = ttk.Button(text="Toggle Update Btn", command=btn3_callback_functor(btn2))
btn3.pack()

window.mainloop()

