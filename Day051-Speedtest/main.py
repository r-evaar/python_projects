import os
from selenium.webdriver import Chrome as Browser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait as w, expected_conditions as ec
from threads import kill_notifications
from threading import Thread
from selenium.webdriver.common.keys import Keys
import keyboard

DOWN_SPEED = 250
UP_SPEED = 150

options = Options()
options.add_argument('--incognito')
options.add_argument("--window-size=1280,720")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-geolocation")

service = Service(executable_path='../../chromedriver.exe')
service.start()

driver = Browser(service=service, options=options)
Thread(target=kill_notifications(driver)).start()

driver.get(url='https://www.speedtest.net/')

go = driver.find_element(By.CLASS_NAME, "start-text")
go.click()

wait = w.WebDriverWait(driver, timeout=120)

results_event = ec.presence_of_element_located((By.CLASS_NAME, 'result-container-speed-active'))
results = wait.until(results_event)
down_speed, up_speed = \
    [float(results.find_element(By.CLASS_NAME, cn).text) for cn in ['download-speed', 'upload-speed']]

driver.get('https://www.twitter.com')

login = driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]')
login.click()

wait._timeout = 10

login_event = ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-labelledby="modal-header"]'))
div = wait.until(login_event)
entry = div.find_element(By.TAG_NAME, 'input')

entry.send_keys(os.environ.get('TWITTER_USR'))

next_ = div.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
next_.click()

password = driver.switch_to.active_element
password.send_keys(os.environ.get('TWITTER_PSS'), Keys.ENTER)

pass
