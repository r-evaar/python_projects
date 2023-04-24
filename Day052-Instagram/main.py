import os
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait as w, expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

driver = Chrome()
driver.get("https://www.instagram.com")

wait = w.WebDriverWait(driver, timeout=10)

def get_element(by, id_, condition=ec.presence_of_element_located):
    event = condition((by, id_))
    return wait.until(event)

# --- Sign in -------------------------------------------------------- #
selectors = ['input[aria-label="Phone number, username, or email"]', 'input[aria-label="Password"]', 'button[type="submit"]']

usr, psw, btn = [get_element(By.CSS_SELECTOR, selector) for selector in selectors]

usr.send_keys(os.environ.get('INS_USR'))
psw.send_keys(os.environ.get('INS_PSW'))
btn.click()

driver.maximize_window()
wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Instagram"]')))

# --- Target account ------------------------------------------------- #

driver.get('https://www.instagram.com/mrwhosetheboss/')

btn = get_element(By.CSS_SELECTOR, 'a[href="/mrwhosetheboss/followers/"]', condition=ec.element_to_be_clickable)
btn.click()

div = get_element(By.CSS_SELECTOR, 'div[class="_aano"]')

sleep(2)

actions = ActionChains(driver)
modal = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')
for i in range(3):
    follows = div.find_elements(By.CSS_SELECTOR, "._acan._acap._acas._aj1-")

    for follow in follows:
        if follow.text == 'Follow':
            follow.click()

    actions.move_to_element(modal).perform()
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)

    sleep(10)

driver.quit()
