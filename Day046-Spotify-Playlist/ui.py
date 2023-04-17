import os
import tkinter as tk
from queue import Queue
from tkinter import Tk, messagebox
from opt import *
from threading import Thread, Lock
from ui_threading import ValidateSubmission, CreatePlaylist
from datetime import datetime
from utils import button, request_songs, to_spotify
from tkinter import ttk

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class App:

    # Required for closing the app when 'ui_threading' functions are used
    def destroy(self):
        self.is_running = False

    @staticmethod
    def date_validation(sect):
        common = lambda x: x.isdigit()  # All day/month/year entries must be digits

        # Additional constrains per entry type
        if sect == 'day':
            sub = lambda x: 0 <= int(x) <= 31
        elif sect == 'month':
            sub = lambda x: 0 <= int(x) <= 12
        elif sect == 'year':
            sub = lambda x: 0 <= int(x) <= datetime.today().year

        # Combine common and specialized validation constrains.
        def validation_fun(entry):
            try:
                return common(entry) and sub(entry) or entry == ""
            except ValueError:
                return False

        return validation_fun

    def __init__(self):

        # --- Attributes ------------------------------------------------------#
        self.is_running = True
        self.hold = False
        self.fields = ['day', 'month', 'year']
        self.cache = 'token.txt'
        self.uri_queue, self.v_queue = Queue(), Queue()
        self.lock = Lock()
        self.songs = []

        # --- Initialization --------------------------------------------------#
        root = Tk()

        date = {}
        for field in self.fields:
            validator = (root.register(self.date_validation(field)), '%P')
            var = tk.StringVar(value='')
            date[field] = {
                'label': tk.Label(font=FONT_TXT, text=field.upper()),
                'value': tk.Entry(font=FONT_TXT, width=15, validate='key',
                                  textvariable=var, validatecommand=validator),
                'var': var
            }

        submit = button(text="Submit")
        var = tk.DoubleVar(value=0)
        progress = {
            'label': tk.Label(font=FONT_BAR, text='Waiting'),
            'bar': ttk.Progressbar(orient="horizontal", length=500, mode="determinate", variable=var, takefocus=True),
            'var': var
        }

        # --- Configuration ---------------------------------------------------#
        x = (root.winfo_screenwidth() - W) // 2
        y = (root.winfo_screenheight() - H) // 2
        root.geometry(f"{W}x{H}+{x}+{y}")
        root.protocol("WM_DELETE_WINDOW", self.destroy)
        root.resizable(False, False)
        root.title('Spotify 100 Songs')

        date['day']['value'].focus_set()

        submit.configure(width=71, font=FONT_BTN, takefocus=0,
                         fg=CLR_BTN, bg=CLR_BTN_BG, relief='flat', borderwidth=0,
                         activebackground=CLR_BTN, activeforeground=CLR_BTN_BG,
                         disabledforeground='#bfbfbf')

        # --- Rendering -------------------------------------------------------#
        spacing = 0.3
        x, y = 0.075-spacing, 0.05
        for item in date.values():
            x += spacing
            item['label'].place(relx=x, rely=y)
            item['value'].place(relx=x, rely=y+0.15)

        x, y = 0.075, y+0.4
        submit.place(relx=x, rely=y)

        y += 0.3
        progress['bar'].place(relx=x, rely=y, anchor='w')
        y += 0.15
        progress['label'].place(relx=x, rely=y, anchor='w')

        # --- Callbacks -------------------------------------------------------#
        submit.configure(command=self.submit_callback)

        bindings = [
            lambda _: date['month']['value'].focus_set(),
            lambda _: date['year']['value'].focus_set(),
            lambda _: submit.invoke()
        ]

        for field, binding in zip(self.fields, bindings):
            date[field]['value'].bind('<Right>', binding)
            date[field]['value'].bind('<Return>', binding)

        # --- Threads ---------------------------------------------------------#
        self.root = root
        self.date = date
        self.submit = submit
        self.progress = progress
        Thread(target=ValidateSubmission(self)).start()
        Thread(target=CreatePlaylist(self)).start()

        # --- Startup ---------------------------------------------------------#
        tk.mainloop()

    def setup_spotipy(self):
        # Authentication
        auth_manager = SpotifyOAuth(
            client_id=os.environ.get('SPOTIFY_ID'),
            client_secret=os.environ.get('SPOTIFY_SECRET'),
            redirect_uri='http://localhost:8080',
            scope="playlist-modify-private",
            show_dialog=True,
            cache_path=self.cache
        )

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        user_info = self.sp.current_user()
        self.user_id = user_info['id']

    def submit_callback(self):
        try:
            self.setup_spotipy()
        except Exception as e:
            if os.path.isfile(self.cache):
                os.remove(self.cache)
                self.setup_spotipy()
            else:
                raise e
        try:
            self.hold = True
            self.toggle_submit(False)

            for key, item in self.date.items():
                if key == 'year':
                    fmt = '4'
                    if int(item['var'].get()) < 1960:
                        item['var'].set('1960')
                else:
                    fmt = '2'
                item['var'].set(f"{int(item['var'].get()):0{fmt}d}")

            self.root.update()
            self.songs = request_songs(self.date)
            to_spotify(self)

        except Exception as e:
            messagebox.showerror(title="Error", message=e.__str__())

    def toggle_submit(self, on):
        if not self.is_running: return
        if on and not self.hold:
            if self.submit['state'] == tk.DISABLED:
                self.submit.config(state=tk.NORMAL, bg=CLR_BTN_BG)
        else:
            self.submit.config(state=tk.DISABLED, bg='#e0dede')
        self.root.update()
