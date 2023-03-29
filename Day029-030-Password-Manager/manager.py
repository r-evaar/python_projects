import abc
import json
import os.path
import subprocess
import tkinter as tk
from pandas import read_json
from tkinter import ttk, messagebox
from options import *
from random import choice
from threading import Thread
from queue import SimpleQueue
from time import sleep
from pyperclip import copy

class BackendThread:

    num_active_threads = 0
    queue = None
    active = True

    def __init__(self, queue):
        BackendThread.queue = queue
        BackendThread.num_active_threads += 1

    def __call__(self):
        while True:
            if self.queue.empty() and self.active:  # Do some backend work, no queue msg (App is still running)
                sleep(1e-4)  # Allow GUI interactivity
                self.main()
            else:
                self.terminate()
                break

    @abc.abstractmethod
    def main(self):
        pass

    def terminate(self):

        if self.active:
            BackendThread.num_active_threads -= 1
            self.active = False

        if self.num_active_threads > 0:
            return

        msg = self.queue.get()  # Perform the close request

        if type(msg) is PasswordManagerApp:
            msg.destroy()  # Requires @destroy override as defined later.
            # Default destroy causes this thread to stuck
            # hear and never terminate

        self.queue.put(1)  # Resent an arbitrary message to other threads to terminate.


class check_input_func(BackendThread):

    def __init__(self, fields, btns, queue):
        super().__init__(queue)
        self.fields = fields
        self.btns = btns

    @staticmethod
    def toggle_button(btn, condition):
        if condition:
            state = btn['state']
            if type(state) is not str:
                state = state.string
            if state == tk.DISABLED:
                btn.configure(state=tk.NORMAL)
        else:
            btn.configure(state=tk.DISABLED)

    def main(self):
        add_allowed = not (True in [field.get() in ['', DEFAULT_EMAIL] for field in self.fields])
        self.toggle_button(self.btns['add'], add_allowed)

        passwords_available = os.path.isfile(f'./{DATA_FILE}')
        if passwords_available:
            try:
                passwords_available = not read_json(DATA_FILE).empty
            except (PermissionError, ValueError):
                passwords_available = False

        self.toggle_button(self.btns['view'], passwords_available)

class check_database_func(BackendThread):

    def __init__(self, fields, add_btn, queue):
        super().__init__(queue)
        self.fields = fields
        self.add_btn = add_btn
        self.updated = False

    def main(self):
        if not os.path.isfile(DATA_FILE):
            file = open(DATA_FILE, 'w')
            file.close()

        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
            except (PermissionError, ValueError):
                return

        website = self.fields['website'].get().lower()
        if website in data:
            info = data[website]
            if not self.updated:
                self.fields['pass'].delete(0, tk.END)
                self.fields['email'].delete(0, tk.END)

                self.fields['email'].insert(0, info['email'])
                self.fields['pass'].insert(0, info['password'])

                self.add_btn.configure(text='Update')

            self.updated = True

        else:
            self.updated = False
            if self.add_btn.cget('text') == 'Update':
                self.add_btn.configure(text='Add')

class default_empty_email(BackendThread):

    def __init__(self, field, queue):
        super().__init__(queue)
        self.field = field

    def main(self):
        has_focus = self.field.focus_get() == self.field

        if self.field.get() == '' and not has_focus:
            self.field.insert(0, DEFAULT_EMAIL)
            self.field.configure(fg=CLR_DF)

        if self.field.get() == DEFAULT_EMAIL and has_focus:
            self.field.delete(0, tk.END)

        if self.field.get() != DEFAULT_EMAIL:
            self.field.configure(fg=CLR_TX)

class PasswordManagerApp(tk.Tk):

    def close_request(self):
        self.backend.put(self)

    def __init__(self, backend_queue):
        super().__init__()

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
        img = tk.PhotoImage(file='./logo.png')
        main_canvas = tk.Canvas(width=img.width(), height=img.height(), highlightthickness=0, bg=CLR_BG)

        main_canvas.img = img  # We have to keep a canvas reference to the PhotoImage
        main_canvas.create_image(0, 2, image=img, anchor='nw')
        main_canvas.place(relx=0.5, rely=0.3, anchor='center')

        website_lbl = ttk.Label(text="Website:", style='My.TLabel')
        website_lbl.place(relx=0.1, rely=0.6, anchor='w')

        email_lbl = ttk.Label(text="Email/Username:", style='My.TLabel')
        email_lbl.grid(row=2, column=0)
        email_lbl.place(relx=0.1, rely=0.675, anchor='w')

        self.website_txt = tk.Entry(font=FONT_TXT, width=40)
        self.website_txt.focus()
        self.website_txt.place(relx=LEFT_IN_EDGE, rely=0.6, anchor='w')
        self.website_txt.bind('<Return>', lambda _: self.email_txt.focus_set())

        self.email_txt = tk.Entry(font=FONT_TXT, width=40)
        self.email_txt.place(relx=LEFT_IN_EDGE, rely=0.675, anchor='w')
        self.email_txt.bind('<Return>', lambda _: self.pass_txt.focus_set())

        self.pass_txt = tk.Entry(font=FONT_TXT, width=20)
        self.pass_txt.place(relx=LEFT_IN_EDGE, rely=0.75, anchor='w')
        self.pass_txt.bind('<Return>', lambda _: self.add_btn.invoke())

        pass_lbl = ttk.Label(text="Password:", style='My.TLabel')
        pass_lbl.place(relx=0.1, rely=0.75, anchor='w')

        generate_btn = ttk.Button(style='My.TButton', text="Generate Password",
                                  width=20, takefocus=0, command=self.gen_password)
        generate_btn.place(relx=0.9, rely=0.75, anchor='e')
        generate_btn.configure(state=tk.NORMAL, takefocus=0)

        add_btn = ttk.Button(style='My.TButton', text="Add", state=tk.DISABLED,
                             width=45, takefocus=0, command=self.export)
        add_btn.place(relx=LEFT_IN_EDGE-0.001, rely=0.825, anchor='w')
        self.add_btn = add_btn

        view_btn = ttk.Button(style='My.TButton', text='View Passwords', state=tk.DISABLED,
                              width=16, takefocus=0, command=self.open_passwords)
        view_btn.place(relx=0.1, rely=0.825, anchor='w')

        # Password characters
        self.chars = []
        for r in [(33, 41), (48, 57), (65, 91), (97, 122)]:
            self.chars += [chr(n) for n in range(r[0], r[1])]

        # Backend Processes
        btns = {'add': add_btn, 'view': view_btn}
        fields_monitor = check_input_func((self.email_txt, self.website_txt, self.pass_txt), btns, backend_queue)
        Thread(target=fields_monitor).start()

        fields = {'website': self.website_txt, 'email': self.email_txt, 'pass': self.pass_txt}
        auto_pass_search = check_database_func(fields, add_btn, backend_queue)
        Thread(target=auto_pass_search).start()

        update_email = default_empty_email(self.email_txt, backend_queue)
        Thread(target=update_email).start()

    def search(self):
        pass

    @staticmethod
    def open_passwords():
        subprocess.run(['start', DATA_FILE], shell=True)

    def gen_password(self):
        password = ''.join([choice(self.chars) for _ in range(PASS_LEN)])
        self.pass_txt.delete(0, tk.END)
        self.pass_txt.insert(0, password)
        copy(password)

    def export(self):
        email = self.email_txt.get().lower()
        password = self.pass_txt.get()
        site = self.website_txt.get().lower()

        if self.add_btn.cget('text') == "Add":
            prompt = "Save credentials?"
        else:
            prompt = "Overwrite current credentials?"

        msg = "These are the detailed entered:\n"\
              f"Email: {email}\n"\
              f"Password: {self.pass_txt.get()}\n\n"\
              + prompt

        if not messagebox.askyesno(title=site.upper(), message=msg):
            return

        new_data = {
            site: {
                'email': email,
                'password': password
            }
        }

        if not os.path.isfile(DATA_FILE):
            file = open(DATA_FILE, 'w')
            file.close()

        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                data.update(new_data)
            except json.decoder.JSONDecodeError:
                data = new_data

        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=True)

            self.website_txt.delete(0, tk.END)
            self.pass_txt.delete(0, tk.END)

        messagebox.showinfo(title="Success", message="Password Saved!")

    def destroy(self) -> None:
        for c in list(self.children.values()): c.destroy()
        self.tk.call('destroy', self._w)

if __name__ == '__main__':
    termination_queue = SimpleQueue()
    app = PasswordManagerApp(termination_queue)
    app.mainloop()

