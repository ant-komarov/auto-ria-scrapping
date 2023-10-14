from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from parser.utilities import (
    get_last_page,
    get_links_from_page,
    get_username,
    get_car_number,
    get_car_vin,
    get_phone_number, accept_cookies
)


def get_cars_list(url: str, driver: webdriver) -> list[str]:
    car_links = []
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    last_page = get_last_page(soup)

    for i in range(1, last_page):
        print(f"Collecting links from page {i}")
        driver.get(url + f"?page={i}")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        car_links += get_links_from_page(soup)

    return car_links


def get_car_info(url: str, driver: webdriver) -> dict | None:
    car_info = {}
    driver.get(url)
    sleep(0.25)
    accept_cookies(driver)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    removed = soup.select_one("div#autoDeletedTopBlock")
    if removed:
        return None
    car_info["url"] = url
    car_info["title"] = soup.select_one("h1.head")["title"]
    car_info["price_usd"] = int(
        soup.select_one("div.price_value>strong").text.replace(" ", "").replace("$", "").replace("€", "")
    )
    car_info["odometer"] = int(soup.select_one("span.size18").text) * 1000
    car_info["username"] = get_username(driver)
    car_info["image_url"] = soup.select_one("img.outline.m-auto")["src"]
    car_info["images_count"] = int(soup.select_one("span.count > span.mhide").text.split()[-1])
    car_info["car_number"] = get_car_number(driver)
    car_info["car_vin"] = get_car_vin(driver)
    car_info["phone_number"] = get_phone_number(driver)

    return car_info
