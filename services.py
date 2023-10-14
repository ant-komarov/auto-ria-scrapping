import json
from datetime import datetime

from sqlalchemy.orm import Session

from db.models import Car


def save_car_to_db(car_data: dict, db: Session):
    db_car = Car(**car_data)
    db.add(db_car)
    db.commit()
    db.close()


def dump_from_db(db: Session):
    cars = db.query(Car).all()
    car_data = []
    for car in cars:
        car_data.append({
            "id": car.id,
            "url": car.url,
            "title": car.title,
            "price_usd": car.price_usd,
            "odometer": car.odometer,
            "username": car.username,
            "phone_number": car.phone_number,
            "image_url": car.image_url,
            "images_count": car.images_count,
            "car_number": car.car_number,
            "car_vin": car.car_vin,
            "datetime_found": car.datetime_found.isoformat()
        })
    db.close()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f"dumps/{timestamp}_dump.json"

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(car_data, json_file, ensure_ascii=False, indent=4)

    print("All data dumped to file")
    db.query(Car).delete()
    db.commit()
    db.close()
