import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
from tkinter import Image
from PIL import ImageTk
from threading import Thread

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

def request_songs(date):
    d, m, y = [date[i]['value'].get() for i in ['day', 'month', 'year']]
    date_str = f"{y}-{m}-{d}"

    url = f"https://www.billboard.com/charts/hot-100/{date_str}/"
    response = requests.get(url=url)

    try:
        response.raise_for_status()
    except Exception as e:
        assert type(e) == requests.exceptions.HTTPError
        messagebox.showerror(title='Error', message=e.__str__())
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = [element for element in soup.select('.o-chart-results-list-row')]
    songs = []
    for element in elements:
        sub_soup = BeautifulSoup(element.__str__(), 'html.parser')
        song = {
            'rank': int(sub_soup.select_one('.c-label').text.strip()),
            'name': sub_soup.select_one('.c-title').text.strip()
        }
        songs.append(song)

    return {'date': date_str, 'list': songs}

def to_spotify(app):

    # --- Multi-Threaded O(n) search using Spotify API Queries ----------- #
    app.progress['label'].update()
    start_threads(app)

def start_threads(app):
    for song in app.songs['list']:
        Thread(
            target=song_search,
            args=(song, app)
        ).start()

def song_search(song, app):
    try:
        app.lock.acquire()
        p = app.progress['var'].get()
        app.root.update()
        app.lock.release()

        app.progress['var'].set(p + 1)
        app.progress['label']['text'] = f"Searching ({int(p) + 1:03d}%) - {song['name']}"

        song_uri = app.sp.search(song['name'], limit=1, type='track')['tracks']['items'][0]['uri']
        app.uri_queue.put({'rank': song['rank'], 'uri': song_uri})
    except IndexError:
        print(f"Couldn't find results for: {song['name']}")
    except Exception as e:
        if not app.is_running:
            return
        else:
            raise e
    finally:
        app.v_queue.put(0)
