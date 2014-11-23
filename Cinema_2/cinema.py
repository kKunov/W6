from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from datetime import datetime
Base = declarative_base()


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
    date = Column(DateTime)


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


def make_db():
    session.add_all([
        Movie(name='The Hunger Games: Catching Fire', rating=7.9),
        Movie(name='Wreck-It Ralph', rating=7.8),
        Movie(name='Her', rating=8.3),
    ])

    session.add_all([
        Projection(movie_id=1, type_movie='3D',
                   date=datetime.strptime('01/04/14 19:10', '%d/%m/%y %H:%M')),
        Projection(movie_id=1, type_movie='2D',
                   date=datetime.strptime('01/04/14 19:00', '%d/%m/%y %H:%M')),
        Projection(movie_id=1, type_movie='4DX',
                   date=datetime.strptime('02/04/14 21:00', '%d/%m/%y %H:%M')),
        Projection(movie_id=3, type_movie='2D',
                   date=datetime.strptime('05/04/14 20:20', '%d/%m/%y %H:%M')),
        Projection(movie_id=2, type_movie='3D',
                   date=datetime.strptime('02/04/14 22:00', '%d/%m/%y %H:%M')),
        Projection(movie_id=2, type_movie="2D",
                   date=datetime.strptime('02/04/14 19:30', '%d/%m/%y %H:%M'))])
    session.commit()


def main():
    make_db()


if __name__ == '__main__':
    main()
