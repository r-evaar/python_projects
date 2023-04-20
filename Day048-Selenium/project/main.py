from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import keyboard

service = Service(executable_path='../../../chromedriver.exe')
driver = Chrome()

driver.get(url='https://orteil.dashnet.org/cookieclicker/')

wait = WebDriverWait(driver, 10)
for identifier in ["langSelect-EN", ['/html/body/div[1]/div/a[1]'], ['//*[@id="note-1"]/div[3]/h5/a'], "bigCookie"]:
    if type(identifier) == list:
        by = By.XPATH
        identifier = identifier[0]
    else:
        by = By.ID

    while True:
        try:
            presence = ec.presence_of_element_located((by, identifier))
            target = wait.until(presence)
            wait.until(ec.element_to_be_clickable((by, identifier)))
            target.click()
            break
        except (StaleElementReferenceException, ElementClickInterceptedException):
            continue

anchor_tip = driver.find_element(By.ID, 'tooltipAnchor')

def hovering(a):
    style = a.get_attribute('style')
    attributes = {
        key: value.strip(';:') for key, value in [opt.split(': ') for opt in style.split('; ') if opt != '']
    }
    return attributes['display'] != 'none'


def play(cookie, anchor):
    if not hovering(anchor) and not keyboard.is_pressed('ctrl'):
        cookie.click()

try:
    while True:
        play(target, anchor_tip)
except Exception as e:
    print(e.__class__, e)

driver.quit()
