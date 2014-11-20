from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import DATETIME
import datetime

Base = declarative_base()
date_type = DATETIME(
    storage_format="%(day)02d-%(month)02d-%(year)04d %(hour)02d:%(min)02d")


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Float)


class Projection(Base):
    __tablename__ = "projection"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    movie = relationship("Movie", backref="projections")
    type_movie = Column(String)
    date = Column(date_type)


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    UniqueConstraint('username')
    projection_id = Column(Integer, ForeignKey("projection.id"))
    projection = relationship("Projection", backref="reservations")
    row = Column(Integer)
    sit = Column(Integer)


engine = create_engine("sqlite:///cinema.db")
Base.metadata.create_all(engine)

session = Session(bind=engine)

session.commit()


def is_enought_sits(number_of_sits):
    free_sits = session.query(Reservation
                              ).filter(Reservation.projection_id=pr_id).count()
    if number_of_sits == "exit":
        return True
    elif free_sits < number_of_sits:
        return False
    else:
        return True


def is_the_sit_is_free(sit):
    if sit[0] > 10 or sit[0] < 1 or sit[1] > 10 or sit[1] < 1:
        return False



def make_reservation():
    user_name = input("Username: ")
    pr_id = input("Chose projection ID: ")
    number_of_sits = input("How many sits you need: ")
    if is_enought_sits(number_of_sits) is False:
        while is_enought_sits is False:
            print("Not enoght sits left, you can buy less sits?")
            number_of_sits = input("You can exit(tipe: exit) or you can try w\
                ith less sits: ")
    if number_of_sits == "exit":
        return number_of_sits
    sits = [[]]
    for index in range(number_of_sits):
        while is_the_sit_is_free(sits[index]) is False:
            sits[index].append(input("Chose row: "))
            sits[index].append(input("Chose sit: "))
            if is_the_sit_is_free[index] is False:
                print("This sit is already taken or invalid!!! \
                       Try again!")
