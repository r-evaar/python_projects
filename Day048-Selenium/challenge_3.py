from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker
from random import randint

LANG = 'en-US'

def fill_form(d: Chrome):
    fake = Faker()
    while True:
        try:
            first, last = fake.name().split(' ')
            break
        except ValueError: pass

    d.find_element(By.NAME, 'firstName').send_keys(first)
    d.find_element(By.NAME, 'lastName').send_keys(last)

    username = d.find_element(By.NAME, 'Username')

    username.send_keys('a' + Keys.ENTER)
    sleep(1)

    while username.get_attribute('aria-invalid') == 'true':
        username.clear()
        email = f"{fake.email().split('@')[0]}{randint(1000,9999)}"
        username.send_keys(email+Keys.ENTER)
        sleep(1)

    password = fake.password()
    key1 = d.find_element(By.NAME, 'Passwd')
    key2 = d.find_element(By.NAME, 'ConfirmPasswd')
    [key.send_keys(password) for key in [key1, key2]]

    # The 'next' button has the least characters
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    n = [len(button.text) for button in buttons]
    idx = n.index(min(n))
    button = buttons[idx]

    text = button.text
    button.click()

    sleep(5)

    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        if button.text == text:
            button.click()

options = Options()
options.add_argument('--incognito')
options.add_argument(f'--lang={LANG}')
service = Service(executable_path='../../chromedriver.exe')
driver = Chrome(service=service, options=options)

driver.get(url='https://www.google.com/gmail/about/')

btns = driver.find_elements(By.CSS_SELECTOR, '.button')
target = None
for btn in btns:
    try:
        attr = btn.get_attribute('data-action')
        if attr == 'create an account':
            target = btn
            break
    except Exception as e:
        print(f'failed: {e.__str__()}')

if target:
    target.click()
    fill_form(driver)

driver.quit()
