import tkinter as tk
from PIL import Image, ImageTk
from config import CLR_BG, GRAPHICS_PATH
def button(ratio=0.1, **kw):

    if 'img_file' in kw.keys():
        filename_1 = kw['img_file']['release']
        filename_2 = kw['img_file']['press']
        del kw['img_file']
        add_img = True
    else:
        add_img = False

    btn = tk.Button(**kw)

    if add_img:
        img_1 = Image.open(GRAPHICS_PATH+filename_1)
        img_2 = Image.open(GRAPHICS_PATH+filename_2)
        cw, ch, r = img_1.width, img_1.height, ratio
        w = int(cw * r)
        h = int(ch * w / cw)
        img_1 = ImageTk.PhotoImage(img_1.resize((w, h), Image.BICUBIC))
        img_2 = ImageTk.PhotoImage(img_2.resize((w, h), Image.BICUBIC))
        btn.configure(image=img_1, relief='flat', borderwidth=0,
                      activebackground=CLR_BG,
                      takefocus=0, bg=CLR_BG)
        btn.bind('<ButtonRelease-1>', lambda _: btn.configure(image=img_1))
        btn.bind('<Button-1>', lambda _: btn.configure(image=img_2))

        return btn, img_1, img_2

    return btn

