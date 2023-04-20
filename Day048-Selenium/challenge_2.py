from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


url = 'https://en.wikipedia.org/wiki/Main_Page'

options = Options(); options.add_argument('--incognito')
service = Service(executable_path='../../chromedriver.exe')
driver = Chrome(service=service, options=options)

driver.get(url)

articles_count = driver.find_element(By.XPATH, '//*[@id="articlecount"]/a[1]')
articles_count_val = int(articles_count.text.replace(',', ''))

print(articles_count_val)

articles_count.click()

uploaded_files = driver.find_element(By.LINK_TEXT, 'Uploaded files')
uploaded_files.click()

find = lambda x: driver.find_element(By.XPATH, x)
icon = '//*[@id="p-search"]/a'
bar = '//*[@id="searchform"]/div/div/div[1]/input'
try:
    search_bar = find(bar)
except NoSuchElementException:
    wait = WebDriverWait(driver, 10)
    event = lambda x: ec.presence_of_element_located((By.XPATH, x))
    event_icon = event(icon)
    event_bar = event(bar)

    wait.until(event_icon).click()
    search_bar = wait.until(event_bar)

search_bar.send_keys('ChatGPT'+Keys.ENTER)

sleep(5)

driver.quit()
