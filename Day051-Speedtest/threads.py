import abc
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By

class Backend:

    num_active = 0
    num_threads = 0
    active = True
    driver = None

    def __init__(self, driver):
        Backend.driver = driver
        Backend.num_threads += 1
        self.id = Backend.num_threads

    def __call__(self):
        while True:
            self.active = self.main()

            if not self.active:
                self.terminate()
                break

    def terminate(self):
        Backend.num_active -= 1
        if Backend.num_active == 0:
            self.driver.quit()

    @abc.abstractmethod
    def main(self):
        pass

class kill_notifications(Backend):

    def __init__(self, driver):
        super().__init__(driver)

    def main(self):
        try:
            notifications = self.driver.find_elements(By.CSS_SELECTOR, '.notification, .modal-overlay')
            [self.driver.execute_script("arguments[0].remove();", notification) for notification in notifications]

            return True
        except NoSuchWindowException:
            print(f"Stopping thread-{self.id}")
            return False
