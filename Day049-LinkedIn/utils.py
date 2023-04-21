import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait as W, expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as WE

def get_elements(driver, wait_type, identifiers, timeout=10):

    elements = []

    wait = W.WebDriverWait(driver, timeout=timeout)
    for identifier in identifiers:
        event = wait_type((identifier['by'], identifier['value']))
        elements.append(wait.until(event))

    return elements if len(elements) > 1 else elements[0]

def sign_in(driver):

    wait_type = EC.presence_of_element_located
    identifiers = [
        {'by': By.ID, 'value': 'session_key'},
        {'by': By.ID, 'value': 'session_password'}
    ]

    username, password = get_elements(driver, wait_type, identifiers)

    username: WE; password: WE  # For debugging autocompletion

    username.send_keys(os.environ.get('LI_U')+Keys.ENTER)
    password.send_keys(os.environ.get('LI_P')+Keys.ENTER)

def click_jobs(driver):

    job_icon = get_elements(
        driver, EC.presence_of_element_located,
        [{'by': By.CSS_SELECTOR, 'value': 'a[href="https://www.linkedin.com/jobs/?"]'}]
    )

    job_icon.click()

    # Wait till jobs page loads
    get_elements(
        driver, EC.presence_of_element_located,
        [{'by': By.CLASS_NAME, 'value': 'jobs-home-scalable-nav'}]
    )


def click_search_icon(driver):

    search_icon = get_elements(
        driver, EC.element_to_be_clickable,
        [{'by': By.ID, 'value': 'global-nav-search'}]
    )

    search_icon.click()

def search(driver, query):
    search_bar = get_elements(
        driver, EC.presence_of_element_located,
        [{'by': By.CLASS_NAME, 'value': 'jobs-search-box__text-input'}]
    )

    search_bar.send_keys(query+Keys.ENTER)

def click_easy_apply(driver):

    easy_apply = get_elements(
        driver, EC.element_to_be_clickable,
        [{'by': By.CSS_SELECTOR, 'value': 'button[aria-label="Easy Apply filter."]'}]
    )

    easy_apply.click()


