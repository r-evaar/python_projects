from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

url = 'https://www.python.org/'
driver_path = '../../chromedriver.exe'

service = Service(executable_path=driver_path)
options = Options()
options.add_argument('--incognito')

driver = Chrome(service=service, options=options)

driver.get(url=url)

# ----------------------------------------------- #

event_items_selector = '.event-widget .menu li'
event_items = driver.find_elements(By.CSS_SELECTOR, event_items_selector)

events = []
frmt = '%Y-%m-%dT%H%M%S%z'
for item in event_items:
    date = item.find_element(By.TAG_NAME, 'time')
    dt_str = date.get_attribute('datetime').replace(':', '')
    dt = datetime.strptime(dt_str, frmt)

    event = item.find_element(By.TAG_NAME, 'a')
    title = event.text
    link = event.get_attribute('href')

    events.append({
        'title': title,
        'date': dt,
        'link': link
    })

[print(event) for event in events]
