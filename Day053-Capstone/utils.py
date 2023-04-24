from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import wait as w, expected_conditions as ec
import requests

FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLScEkPTvBeo-AcCWzzQLqM3-hG7yfzOv0Ju55e0LjfkPExPEVA/viewform?usp=sf_link'

def scrap_data(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US'
    }

    response = requests.get(url=query, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    search_list = soup.select_one('#grid-search-results')

    items = search_list.find_all('li')
    items = filter_items(items)

    return [get_info(item) for item in items]

def get_info(item):
    description = item.find('a')
    address = description.find('address').text
    link = 'https://www.zillow.com/'+description.get('href')
    price = item.find('span').text.split('+')[0].split('/')[0]

    return {'address': address, 'link': link, 'price': price}

def filter_items(items):
    out = []
    for item in items:
        try:
            exist = 'ListItem' in item.get('class')[0] and item.find('a') is not None
        except:
            exist = False
        if exist:
            out.append(item)
    return out

def fill_forms(data):

    for item in data:
        driver = Chrome()
        driver.get(FORM_LINK)

        address, price, link, submit = get_form_elements(driver)

        address.send_keys(item['address'])
        price.send_keys(item['price'])
        link.send_keys(item['link'])

        submit.click()

        driver.quit()


def get_form_elements(driver):
    divs = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    entries = [div.find_element(By.TAG_NAME, 'input') for div in divs]

    wait = w.WebDriverWait(driver, timeout=5)
    submit = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[0]

    event = ec.element_to_be_clickable(submit)
    wait.until(event)

    entries.append(submit)
    return entries

