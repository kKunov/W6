from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import DATETIME

Base = declarative_base()
date_type = DATETIME(
    storage_format="%(day)02d-%(month)02d-%(year)04d")
time_type = DATETIME(
    storage_format="%(hour)02d:%(min)02d")


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
    time = Column(time_type)


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
session.add_all([
    Movie(name="The Hunger Games: Catching Fire", rating=7.9),
    Movie(name="Wreck-It Ralph", rating=7.8),
    Movie(name="Her", rating=8.3)])
session.commit()
