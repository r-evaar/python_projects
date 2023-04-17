import abc
import pandas as pd
from time import sleep
from opt import *

class BackendThread:

    num_threads = 0
    num_active_threads = 0
    app = None
    active = True

    def __init__(self, app):
        BackendThread.app = app
        BackendThread.num_active_threads += 1
        BackendThread.num_threads += 1
        self.id = BackendThread.num_threads

    def __call__(self):
        while True:
            if self.app.is_running and self.active:  # Do some backend work, no queue msg (App is still running)
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

        # Destroy app after all threads are stopped
        for c in list(self.app.root.children.values()): c.destroy()
        self.app.root.tk.call('destroy', self.app.root._w)


class ValidateSubmission(BackendThread):

    def __init__(self, app):
        super().__init__(app)

    def main(self):
        valid = all([sect['value'].get() != "" and int(sect['value'].get()) != 0 for sect in self.app.date.values()])
        self.app.toggle_submit(valid)

class CreatePlaylist(BackendThread):
    def __init__(self, app):
        super().__init__(app)

    def main(self):

        # --- Create Spotify playlist using the 100 URI list --------- #
        len_q = self.app.v_queue.qsize()
        if len_q < 100:
            return

        # Consume v_queue: used only to determine completion
        [self.app.v_queue.get() for _ in range(len_q)]

        uri_list = []
        len_q = self.app.uri_queue.qsize()
        for i in range(len_q):
            uri_list.append(self.app.uri_queue.get())

        playlist = self.app.sp.user_playlist_create(self.app.user_id, self.app.songs['date'], public=False)
        df = pd.DataFrame(data=uri_list)
        df.sort_values(by='rank', inplace=True)
        self.app.sp.playlist_add_items(playlist['id'], df['uri'].to_list())

        # --- Reset UI --------- #
        self.app.progress['var'].set(0)
        self.app.progress['label']['text'] = "waiting"
        self.app.root.update()

        self.app.toggle_submit(True)
        self.app.hold = False
