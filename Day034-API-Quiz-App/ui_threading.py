import abc
from time import sleep

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