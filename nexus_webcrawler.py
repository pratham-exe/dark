from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import re

tor_browser_path = "/home/pratham/Downloads/tor-browser/Browser/firefox"
geckodriver_path = "/usr/bin/geckodriver"


def driver_setup():
    firefox_options = Options()
    firefox_options.binary_location = tor_browser_path
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference('network.proxy.socks_remote_dns', True)
    firefox_options.profile = profile

    service = Service(executable_path=geckodriver_path, log_path="geckodriver.log")

    return firefox_options, service


def get_category_links(driver):
    class_names = driver.find_elements(By.CLASS_NAME, "text-secondary")
    pattern = r'^http://nexusma2isutrqi4ineftrzqzui7tefsyeonxsttsnwzdxxpxay26eqd.onion/products/[^/]+$'
    category_elements = [elem for elem in class_names if "hover:text-base-500" in elem.get_attribute("class") and "duration-[750ms]" not in elem.get_attribute("class") and "text-sm" in elem.get_attribute("class") and re.fullmatch(pattern, elem.get_attribute("href"))]
    categories = [ele.get_attribute("href") for ele in category_elements]
    return categories


def get_next_page(driver, next_page_no):
    xpath = f"//*[contains(@aria-label, 'Go to page {next_page_no}')]"
    next_page = driver.find_element(By.XPATH, xpath)
    return next_page.get_attribute("href")


def get_product_links(driver):
    class_names = driver.find_elements(By.CLASS_NAME, "line-clamp-3")
    product_links = [product.get_attribute("href") for product in class_names]
    return product_links


def get_last_page(driver):
    xpath = "//*[contains(@aria-label, 'Go to page')]"
    pages = driver.find_elements(By.XPATH, xpath)
    page_nos = [page.text for page in pages]
    products = get_product_links(driver)
    if page_nos:
        return page_nos[-1].strip()
    elif products:
        return 1
    else:
        return 0


def get_shipping_details(driver):
    try:
        shipping_details = driver.find_element(By.CSS_SELECTOR, ".text-secondary.font-normal.mb-3")
    except Exception:
        try:
            shipping_details = driver.find_element(By.CSS_SELECTOR, ".text-primary.font-medium.mb-4")
        except Exception:
            shipping_details = "None"
    return shipping_details


def get_info(driver, info_list, category_link):
    title_name = driver.find_elements(By.TAG_NAME, "h1")
    info_list.append(title_name[1].text)
    xpath_category = "//*[contains(@class, 'hover:text-base-500') and contains(@class, 'duration-[750ms]')]"
    category_list = driver.find_elements(By.XPATH, xpath_category)
    category = [cat.text for cat in category_list if re.fullmatch(category_link, cat.get_attribute("href"))]
    info_list.append(category[0].strip())
    price_class = driver.find_elements(By.CLASS_NAME, "text-green-500")
    price_list = [unit.text for unit in price_class]
    info_list.append(price_list[0])
    availability_class = driver.find_elements(By.CSS_SELECTOR, ".order-first.text-sm.font-semibold.tracking-tight.text-primary")
    info_list.append(availability_class[2].text)
    info_list.append(price_list[1])
    shipping_details = get_shipping_details(driver)
    info_list.append(shipping_details.text)
    info_list.append(title_name[2].text)
    info_list.append(availability_class[4].text)
    activity = driver.find_element(By.CSS_SELECTOR, ".text-sm.text-center.text-secondary.font-light")
    info_list.append(activity.text)
    return info_list
