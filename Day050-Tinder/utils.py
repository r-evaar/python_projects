from selenium.webdriver.support import wait as w
def get_elements(driver, wait_type, identifiers, timeout=10):

    elements = []

    wait = w.WebDriverWait(driver, timeout=timeout)
    for identifier in identifiers:
        event = wait_type((identifier['by'], identifier['value']))
        elements.append(wait.until(event))

    return elements if len(elements) > 1 else elements[0]