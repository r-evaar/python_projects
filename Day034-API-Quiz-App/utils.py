import tkinter as tk
import requests
from PIL import Image, ImageTk

def get_api_data(endpoint, p=None): r = requests.get(url=endpoint, params=p); r.raise_for_status(); return r.json()

def button(ratio=1, **kw):

    if 'img_file' in kw.keys():
        filename_1 = kw['img_file']['release']
        filename_2 = kw['img_file']['press']
        del kw['img_file']
        add_img = True
    else:
        add_img = False

    btn = tk.Button(**kw)

    if add_img:
        img_1 = Image.open(filename_1)
        img_2 = Image.open(filename_2)
        cw, ch, r = img_1.width, img_1.height, ratio
        w = int(cw * r)
        h = int(ch * w / cw)
        img_1 = ImageTk.PhotoImage(img_1.resize((w, h), Image.BICUBIC))
        img_2 = ImageTk.PhotoImage(img_2.resize((w, h), Image.BICUBIC))
        btn.configure(image=img_1, relief='flat', borderwidth=0, takefocus=0, width=w, height=h)
        btn.bind('<ButtonRelease-1>', lambda _: btn.configure(image=img_1))
        btn.bind('<Button-1>', lambda _: btn.configure(image=img_2))

        return btn, img_1, img_2

    return btn
