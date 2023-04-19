from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Constants
CHROME_DRIVER = '../../chromedriver.exe'
PRODUCT = 'https://www.amazon.ae/ASUS-Gaming-GeForce-Graphics-DisplayPort/dp/B0BLGHRCLX/ref=sr_1_1'

# Browser options
chrome_opt: Options = Options()
chrome_opt.add_argument("--incognito")

# Create an interface for Chrome Driver
service = Service(executable_path=CHROME_DRIVER)
driver = webdriver.Chrome(service=service, options=chrome_opt)

# Access the target webpage
driver.get(url=PRODUCT)

# Find HTML element
whole, frac, curr = [
    driver.find_element(By.CSS_SELECTOR, f"#corePriceDisplay_desktop_feature_div .a-price-{i}").text
    for i in ['whole', 'fraction', 'symbol']
]

# Save price
price = {
    'value': float(f"{whole.replace(',', '').replace('.', '')}.{frac}"),
    'currency': curr
}
print(price)

# --- Finding element by XPath ------------- #
xpath = '/html/body/div[2]/div[2]/div[7]/div[3]/div[4]/div[1]/div/h1/span[1]'

try:
    # -- Find element directly (will raise error if element is not yet loaded)
    item_title = driver.find_element(By.XPATH, xpath)

except NoSuchElementException:
    # Initiate a timeout object to wait until the element is loaded
    wait = WebDriverWait(driver, 10)
    # Initiate a <presence> event as an expected condition
    event = ec.presence_of_element_located((By.XPATH, xpath))
    # Execute to get element
    item_title = wait.until(event)

print(item_title.text)

# --- #
print('\n'+'-'*30+'\n')

# --- Finding multiple elements ------------ #
categories = [item.text for item in driver.find_elements(By.CLASS_NAME, 'nav-a')]
[print(item) for item in categories if item != '']

# -- END -------------- #

driver.close()  # Close currently active tab
driver.quit()  # Close the entire browser
