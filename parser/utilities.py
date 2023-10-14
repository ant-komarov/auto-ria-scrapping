from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def get_links_from_page(page_soup: BeautifulSoup) -> list[str]:
    items = page_soup.select("a.m-link-ticket")
    return [item["href"] for item in items]


def accept_cookies(driver: webdriver) -> None:
    try:
        cookie_button = driver.find_element(
            By.CSS_SELECTOR, "label.js-close.c-notifier-btn"
        )
        if cookie_button.is_displayed() and cookie_button.is_enabled():
            cookie_button.click()
    except NoSuchElementException:
        pass


def get_last_page(page_soup: BeautifulSoup) -> int:
    pages = page_soup.select("a.page-link")
    last_page = [page.text for page in pages][-2]
    return int(last_page.replace(" ", ""))


def get_phone_number(driver: webdriver) -> str:
    driver.find_element(
        By.CSS_SELECTOR,
        "#phonesBlock > div > span > a"
    ).click()

    sleep(0.5)

    number = driver.find_element(
        By.CSS_SELECTOR,
        "div.popup-successful-call-desk.size24.bold.green.mhide.green"
    ).get_attribute(
        "data-value"
    ).replace("(", "").replace(")", "").replace(" ", "")
    return "+38" + number


def get_car_number(driver: webdriver) -> str | None:
    number = driver.find_elements(By.CSS_SELECTOR, "span.state-num.ua")
    if number:
        return " ".join(number[0].text.split()[:3])
    return None


def get_car_vin(driver: webdriver) -> str:
    vin = driver.find_elements(By.CSS_SELECTOR, "span.label-vin")
    if vin:
        return vin[0].text
    vin = driver.find_elements(By.CSS_SELECTOR, "span.vin-code")
    return vin[0].text


def get_username(driver: webdriver) -> str:
    username = driver.find_elements(By.CSS_SELECTOR, "div.seller_info_name.bold")

    if username:
        return username[0].text
    username = driver.find_elements(By.CSS_SELECTOR, "h4.seller_info_name")
    return username[0].text
