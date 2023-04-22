import os
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import keyboard

service = Service(executable_path='../../chromedriver.exe')
options = Options()
options.add_argument('--incognito')
options.add_argument("--window-size=1280,720")

driver = Chrome(service=service, options=options)

driver.get('https://mbzuai.ac.ae/')

headers = driver.find_elements(By.CLASS_NAME, 'header__link')

try:
    quick_links = [header for header in headers if header.text == 'Quick links'][0]
except IndexError:
    raise RuntimeError('Cannot access quick links in mbzuai.ac.ae')

actions = ActionChains(driver)
actions.move_to_element(quick_links).perform()  # Hover curser over

# Open calendar in new tab
calendar = driver.find_element(By.LINK_TEXT, 'Academic calendar')
actions.move_to_element(calendar).perform()
actions.context_click(calendar).perform()
keyboard.press('t')

# Switch to the opened tab
driver.switch_to.window(driver.window_handles[1])

fall_path = '/html/body/div/section[2]/div/div[2]/div[2]/div/div[1]/h2'
fall = driver.find_element(By.XPATH, fall_path)
driver.execute_script("arguments[0].scrollIntoView();", fall)
sleep(1)

filename = 'screenshot.png'
driver.maximize_window()
driver.save_screenshot(filename)

os.startfile(filename)

driver.quit()
