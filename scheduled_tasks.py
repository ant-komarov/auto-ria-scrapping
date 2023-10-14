import pytz
from celery import Celery

from celery.schedules import crontab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db.database import SessionLocal
from parser.parser import get_cars_list, get_car_info
from services import dump_from_db, save_car_to_db

app = Celery(
    "cars_parsing",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
app.conf.timezone = pytz.timezone("Europe/Kiev")


BASE_URL = "https://auto.ria.com/uk/car/used/"


@app.task
def start_parsing():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Remote("http://selenium-chrome:4444/wd/hub", options=chrome_options)
    link_list = get_cars_list(BASE_URL, driver)
    for link in link_list:
        car_info = get_car_info(link, driver)
        if car_info is None:
            continue
        print(f"Adding info about car {car_info['title']}")
        save_car_to_db(car_info, db=SessionLocal())
    print("All cars added to db")


@app.task
def start_dump_from_db():
    dump_from_db(db=SessionLocal())


app.conf.beat_schedule = {
    "start_cars_parsing": {
        "task": "scheduled_tasks.start_cars_parsing",
        "schedule": crontab(hour=12, minute=0),
    },
    "start_dump_from_db": {
        "task": "scheduled_tasks.start_dump_from_db",
        "schedule": crontab(hour=0, minute=0),
    },
}


if __name__ == "__main__":
    app.start()
