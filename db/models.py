from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    url = Column(String(511), nullable=False)
    title = Column(String(255), nullable=False)
    price_usd = Column(Integer, nullable=False)
    odometer = Column(Integer, nullable=False)
    username = Column(String(127), nullable=False)
    phone_number = Column(String(15), nullable=False)
    image_url = Column(String(511), nullable=True)
    images_count = Column(Integer, nullable=True)
    car_number = Column(String(16), nullable=True)
    car_vin = Column(String(32), nullable=True)
    datetime_found = Column(DateTime, default=datetime.now())
