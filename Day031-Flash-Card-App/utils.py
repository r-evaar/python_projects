import abc
from time import sleep, time
from config import TIMEOUT

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
                sleep(1e-6)  # Allow GUI interactivity
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


class FlipThread(BackendThread):

    def __init__(self, app):
        super().__init__(app)

    def main(self):
        if not self.app.flipped and len(self.app.words) > 1:
            if time() - self.app.timer > TIMEOUT:
                self.app.set_card('back')


class CompletionThread(BackendThread):

    def __init__(self, app):
        super().__init__(app)

    def main(self):
        if len(self.app.words) == 0:
            self.app.is_running = False

