import os.path
import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
from config import *
from graphics import button
from random import randint
from utils import FlipThread, CompletionThread
from threading import Thread
from time import time, sleep

class FlashCards:

    def destroy(self):
        self.is_running = False

    def __init__(self):

        # -- UI Objects Initialization  ------------------------------------------------- #
        root = tk.Tk()
        card_front = Image.open(GRAPHICS_PATH+"card_front.png")
        card_back = Image.open(GRAPHICS_PATH+"card_back.png")
        card_canvas = tk.Canvas(bg=CLR_BG)
        yes_btn, _, _ = button(ratio=BTN_R, img_file={'release': "yes_btn_normal.png", 'press': "yes_btn_clicked.png"})
        no_btn, _, _ = button(ratio=BTN_R, img_file={'release': "no_btn_normal.png", 'press': "no_btn_clicked.png"})

        # -- Attributes Initialization -------------------------------------------------- #
        self.words = self.load_data()
        self.flipped = False
        self.languages = self.words.keys().to_list()
        self.i = 0
        self.is_running = True
        self.timer = time()

        # -- Configuration  ------------------------------------------------------------- #
        rx = root.winfo_screenwidth()
        ry = root.winfo_screenheight()
        root.geometry(f"{W}x{H}+{int((rx-W)/2)}+{int((ry-H)/2)}")
        root.resizable(False, False)
        root.configure(bg=CLR_BG)
        root.title('Flash Cards')
        root.update_idletasks()
        root.protocol("WM_DELETE_WINDOW", self.destroy)

        cw, ch, r = card_front.width, card_front.height, CARD_R
        w, h = [int(a*r) for a in [cw, ch]]
        x, y = [int(a/2) for a in [w, h]]
        card_front = ImageTk.PhotoImage(card_front.resize((w, h), Image.BICUBIC))
        card_back = ImageTk.PhotoImage(card_back.resize((w, h), Image.BICUBIC))
        card_canvas.configure(width=w, height=h, highlightthickness=0)

        card_img_id = card_canvas.create_image(x, y, image=card_front, anchor='c')
        y_t = h * TITLE_OFFSET
        title_id = card_canvas.create_text(x, y_t, text="English", anchor='n', font=TITLE_FONT)
        y_t = y_t + h * WORD_OFFSET
        word_id = card_canvas.create_text(x, y_t, text="Word", anchor='n', font=WORD_FONT_EN)

        # -- Rendering  ----------------------------------------------------------------- #
        y = 0.41
        card_canvas.place(relx=0.5, rely=y, anchor='center')

        x = 1-(W-card_canvas.winfo_reqwidth())/(2*W)
        y = y + 0.48
        yes_btn.place(relx=x, rely=y, anchor='e')
        no_btn.place(relx=1-x, rely=y, anchor='w')

        # -- Callbacks  ----------------------------------------------------------------- #
        yes_btn.configure(command=self.yes_callback)
        no_btn.configure(command=self.next_word)

        # -- Threads  ------------------------------------------------------------------- #
        Thread(target=FlipThread(self)).start()
        Thread(target=CompletionThread(self)).start()

        # -- Startup -------------------------------------------------------------------- #
        self.root = root
        self.card_front = card_front
        self.card_back = card_back
        self.card_canvas = card_canvas
        self.card_img_id = card_img_id
        self.title_id = title_id
        self.word_id = word_id
        self.yes_btn = yes_btn
        self.no_btn = no_btn

        self.set_card('front')
        self.next_word()

        # FINALLY
        self.root.mainloop()

    @staticmethod
    def load_data():
        if not os.path.isfile(SAVE_PATH):
            words = pd.read_csv(WORDS_PATH)
            words.to_csv(SAVE_PATH, index=False, encoding='utf-8-sig')
        else:
            words = pd.read_csv(SAVE_PATH)
        return words

    def yes_callback(self):

        h = len(self.words)
        index = self.words.iloc[self.i].name
        if h > 2:
            self.words.drop(axis=0, index=index, inplace=True)
        elif h == 2:
            self.words = self.words.drop(index)
        elif h == 1:
            self.complete()
            return

        self.words.to_csv(SAVE_PATH, index=False, encoding='utf-8-sig')
        self.next_word()

    def complete(self):
        self.yes_btn.configure(command=lambda: None)
        self.no_btn.configure(command=lambda: None)

        self.set_card('back')
        self.card_canvas.itemconfig(self.title_id, text="Congratulations!")
        self.card_canvas.itemconfig(self.word_id, text="You've Learned 1000 words", font=COMPL_FONT)
        self.card_canvas.update_idletasks()

        words = pd.read_csv(WORDS_PATH)
        words.to_csv(SAVE_PATH, index=False, encoding='utf-8-sig')

    def next_word(self):
        if self.flipped:
            self.flip_card()
        self.i = randint(0, len(self.words)-1)
        self.set_card('same')

    def flip_card(self):

        if self.flipped:
            # Set card to front
            card = self.card_front
            title = self.languages[0]
            color = 'black'
            font = WORD_FONT_EN
            self.timer = time()
        else:
            # Set card to back
            card = self.card_back
            title = self.languages[1]
            color = 'white'
            font = WORD_FONT_AR

        word = self.words.iloc[self.i][title]

        self.card_canvas.itemconfig(self.card_img_id, image=card)
        self.card_canvas.itemconfig(self.title_id, text=title, fill=color)
        self.card_canvas.itemconfig(self.word_id, text=word, fill=color, font=font)

        self.flipped = not self.flipped

    def set_card(self, side):
        if side == 'front':
            self.flipped = True
        elif side == 'back':
            self.flipped = False
        elif side == 'same':
            self.flipped = not self.flipped
        else:
            raise ValueError(f"expected 'side' to be in ['front', 'back', 'same'], but got {side}")

        self.flip_card()

if __name__ == "__main__":
    app = FlashCards()
