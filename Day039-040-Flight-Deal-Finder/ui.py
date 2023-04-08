import tkinter as tk
from tkinter import Tk, messagebox
from utils import button
from api_management import APIManager
from config import *

FONT = ('Ariel', 12, 'bold')
FONT_E = ('Ariel', 12, 'normal')
W, H = 700, 175

class FlightClubApp:

    def __init__(self):

        # --- UI Components ------------#
        self.root = Tk()
        self.first_name = {
            'label': tk.Label(text="First Name", font=FONT),
            'entry': tk.Entry(font=FONT_E)
        }
        self.last_name = {
            'label': tk.Label(text="Last Name", font=FONT),
            'entry': tk.Entry(font=FONT_E)
        }
        self.email = {
            'label': tk.Label(text="Email", font=FONT),
            'entry': tk.Entry(font=FONT_E)
        }
        self.submit_btn = button(text="Submit", font=FONT)

        # --- Attributes -------------- #
        self.user_manager = APIManager(ep=SHEETY_ENDPOINT+'users', key=SHEETY_KEY,
                                       key_name='Authorization', simulate=False)

        # --- Configuration ----------- #
        x = int((self.root.winfo_screenwidth()-W)/2)
        y = int((self.root.winfo_screenheight()-H)/2)
        self.root.geometry(f"{W}x{H}+{x}+{y}")
        self.root.title("Flight Club")

        self.first_name['entry'].configure(width=18)
        self.last_name['entry'].configure(width=18)
        self.email['entry'].configure(width=50)
        self.submit_btn.configure(width=55, relief='flat', borderwidth=0,
                                  takefocus=0, bg='#89aaad', activebackground='#678487')

        # --- Rendering --------------- #
        self.first_name['label'].place(relx=0.1, rely=0.2, anchor='w')
        self.first_name['entry'].place(relx=0.25, rely=0.2, anchor='w')

        self.last_name['label'].place(relx=0.64, rely=0.2, anchor='e')
        self.last_name['entry'].place(relx=0.9, rely=0.2, anchor='e')

        self.email['label'].place(relx=0.1, rely=0.5, anchor='w')
        self.email['entry'].place(relx=0.9, rely=0.5, anchor='e')

        self.submit_btn.place(relx=0.5, rely=0.8, anchor='center')

        # --- Callbacks --------------- #
        self.submit_btn.configure(command=self.update_users)

        # --- Threading --------------- #

        # --- Startup ----------------- #
        self.root.mainloop()

    def update_users(self):
        row = {
            'user': {
                "firstName": self.first_name['entry'].get(),
                "lastName": self.last_name['entry'].get(),
                "email": self.email['entry'].get()
            }
        }
        self.user_manager.post(row)
        messagebox.showinfo(title='Success', message="New user registered!")
