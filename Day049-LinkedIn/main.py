from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils import sign_in, click_jobs, click_search_icon, search, click_easy_apply

POSITION = 'Python Developer'

options = Options()
options.add_argument('--incognito')
service = Service(executable_path='../../chromedriver.exe')
driver = Chrome(service=service, options=options)

driver.get(url='https://www.linkedin.com')
driver.maximize_window()

sign_in(driver)
click_jobs(driver)
click_search_icon(driver)
search(driver, POSITION)
click_easy_apply(driver)

driver.quit()
