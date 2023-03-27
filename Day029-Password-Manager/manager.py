import os.path
import tkinter as tk
from tkinter import ttk, messagebox
from options import *
from random import choice
from threading import Thread
from queue import SimpleQueue
from time import sleep

class check_input_func:

    def __init__(self, fields, btn, queue):
        self.fields = fields
        self.btn = btn
        self.queue = queue

    def __call__(self):
        while True:
            if self.queue.empty():  # Do some backend work, no queue msg (App is still running)
                btn_status = not (True in ['' == field.get() for field in self.fields])
                sleep(0.01)
                self.btn.configure(state=tk.ACTIVE if btn_status else tk.DISABLED)
            else:
                root = self.queue.get()  # Perform the close request
                root.destroy()  # Requires @destroy override as defined later. Default destroy causes this
                                # thread to stuck hear and never terminate
                break

class PasswordManagerApp(tk.Tk):

    def close_request(self):
        self.backend.put(self)

    def __init__(self, backend_queue):
        super().__init__()

        self.data_file = './data.txt'
        self.backend = backend_queue
        self.protocol("WM_DELETE_WINDOW", self.close_request)

        sw, sh = [self.winfo_screenwidth(), self.winfo_screenheight()]
        self.geometry(f"{W}x{H}+{int(sw/2-W/2)}+{int(sh/2-H/2)}")
        self.title("Password Manager")
        self.resizable(False, False)
        self.config(bg=CLR_BG)

        self.style = ttk.Style(self)
        self.style.configure('My.TButton', foreground=CLR_DK, font=FONT_BTN)
        self.style.configure('My.TLabel', font=FONT_LBL, anchor='w')

        # Logo
        img = tk.PhotoImage(file='logo.png')
        main_canvas = tk.Canvas(width=img.width(), height=img.height(), highlightthickness=0)

        main_canvas.img = img  # We have to keep a canvas reference to the PhotoImage
        main_canvas.create_image(0, 2, image=img, anchor='nw')
        main_canvas.place(relx=0.5, rely=0.3, anchor='center')

        website_lbl = ttk.Label(text="Website:", style='My.TLabel')
        website_lbl.place(relx=0.1, rely=0.6, anchor='w')

        self.website_txt = tk.Entry(font=FONT_TXT, width=40)
        self.website_txt.focus()
        self.website_txt.place(relx=0.9, rely=0.6, anchor='e')

        email_lbl = ttk.Label(text="Email/Username:", style='My.TLabel')
        email_lbl.grid(row=2, column=0)
        email_lbl.place(relx=0.1, rely=0.675, anchor='w')

        self.email_txt = tk.Entry(font=FONT_TXT, width=40)
        self.email_txt.insert(0, 'evaar.iv4@gmail.com')
        self.email_txt.place(relx=0.9, rely=0.675, anchor='e')

        pass_lbl = ttk.Label(text="Password:", style='My.TLabel')
        # pass_lbl.grid(row=3, column=0)
        pass_lbl.place(relx=0.1, rely=0.75, anchor='w')

        generate_btn = ttk.Button(style='My.TButton', text="Generate Password",
                                  width=20, takefocus=0, command=self.gen_password)
        self.pass_txt = tk.Entry(font=FONT_TXT, width=20)

        spacing = self.email_txt.winfo_reqwidth() - \
                  (generate_btn.winfo_reqwidth()+self.pass_txt.winfo_reqwidth())

        generate_btn.place(relx=0.9, rely=0.75, anchor='e')
        self.pass_txt.place(relx=0.9-(generate_btn.winfo_reqwidth()+spacing)/W,
                            rely=0.75, anchor='e')

        add_btn = ttk.Button(style='My.TButton', text="Add", state=tk.DISABLED,
                             width=45, takefocus=0, command=self.export)
        add_btn.place(relx=0.9, rely=0.825, anchor='e')

        # Password characters
        self.chars = []
        for r in [(33, 41), (48, 57), (65, 91), (97, 122)]:
            self.chars += [chr(n) for n in range(r[0], r[1])]

        fields_monitor = check_input_func((self.email_txt, self.website_txt, self.pass_txt), add_btn, backend_queue)
        Thread(target=fields_monitor).start()

    def gen_password(self):
        password = ''.join([choice(self.chars) for _ in range(PASS_LEN)])
        self.pass_txt.delete(0, tk.END)
        self.pass_txt.insert(0, password)

    def export(self):
        if not os.path.isfile(f'./{self.data_file}'):
            with open(self.data_file, 'w') as file:
                file.write(f"website, user, password\n")

        email = self.email_txt.get()
        password = self.pass_txt.get()
        site = self.website_txt.get()
        msg = "These are the detailed entered:\n"\
              f"Email: {email}\n"\
              f"Password: {self.pass_txt.get()}\n"\
              "Continue?"

        if not messagebox.askyesno(title=site, message=msg):
            return

        with open(self.data_file, 'a') as file:
            new_data = f"" \
                       f"{site}, " \
                       f"{email}, " \
                       f"{password}\n"
            file.write(new_data)

            self.website_txt.delete(0, tk.END)
            self.pass_txt.delete(0, tk.END)

        messagebox.showinfo(title="Success", message="Password Saved!")

    def destroy(self) -> None:
        for c in list(self.children.values()): c.destroy()
        self.tk.call('destroy', self._w)

if __name__ == '__main__':
    shared_queue = SimpleQueue()
    app = PasswordManagerApp(shared_queue)
    app.mainloop()

