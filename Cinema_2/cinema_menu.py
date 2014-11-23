from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from cinema import Movie, Projection, Reservation
Base = declarative_base()

engine = create_engine("sqlite:///cinema.db")
Base.metadata.create_all(engine)

session = Session(bind=engine)


def is_enought_sits(number_of_sits, pr_id):
    taken_sits = session.query(Reservation.id
                               ).filter(Reservation.projection_id == pr_id
                                        ).count()
    if number_of_sits == "exit":
        return True
    elif 100 - taken_sits < int(number_of_sits):
        return False
    else:
        return True


def taken_sits_fun(pr_id):
    return session.query(Reservation.row, Reservation.sit
                         ).filter(Reservation.projection_id == pr_id)


def is_the_sit_is_free(sit, pr_id):
    if sit[0] > 10 or sit[0] < 1 or sit[1] > 10 or sit[1] < 1:
        return False
    taken_sits = taken_sits_fun(pr_id)
    for sit1 in taken_sits:
        if sit[0] == sit1[0] and sit[1] == sit1[1]:
            return False
    return True


def print_movies():
    movie_list = session.query(Movie.id, Movie.name, Movie.rating).all()
    for row in movie_list:
        print("ID: %s - Movie: %s - Rating: %s" % (row[0], row[1], row[2]))


def print_projections(mov_id):
    movie_list = session.query(Projection.id, Movie.name,
                               Projection.type_movie, Projection.date
                               ).outerjoin(Movie
                                           ).filter(Projection.
                                                    movie_id == mov_id)
    for row in movie_list:
        print("ID: %s, Movie: %s, Type: %s, Date and Time: %s" %
             (row[0], row[1], row[2], row[3]))


def print_sits(pr_id, chosed):
    print(" r\s 1 2 3 4 5 6 7 8 9 10")
    printer = []
    for row in range(10):
        for sit in range(10):
            if ([row+1, sit+1] not in chosed and
                    is_the_sit_is_free([row+1, sit+1], pr_id) is True):
                if sit == 0:
                    printer.append(['.'])
                else:
                    printer[row].append('.')
            else:
                if sit == 0:
                    printer.append(['x'])
                else:
                    printer[row].append('x')
    for row in range(10):
        if row < 9:
            print(" %s   %s %s %s %s %s %s %s %s %s %s" % ((row + 1),
                  printer[row][0], printer[row][1], printer[row][2],
                  printer[row][3], printer[row][4], printer[row][5],
                  printer[row][6], printer[row][7], printer[row][8],
                  printer[row][9]))
        else:
            print(" %s  %s %s %s %s %s %s %s %s %s %s" % ((row + 1),
                  printer[row][0], printer[row][1], printer[row][2],
                  printer[row][3], printer[row][4], printer[row][5],
                  printer[row][6], printer[row][7], printer[row][8],
                  printer[row][9]))


def fin_print(movie_id, pr_id, chosed):
    movie = session.query(Movie.name).filter(Movie.id == movie_id).one()
    date = session.query(Projection.date).filter(Projection.id == pr_id).one()
    type_mov = session.query(Projection.type_movie
                             ).filter(Projection.id == pr_id).one()
    print("Your reservation is:")
    print("Movie: %s" % movie)
    print("Date and Time: %s (%s)" % (date, type_mov))
    print("Seats: %s" % chosed)


def make_reservation():
    user_name = input("Username: ")
    print_movies()
    movie_id = input("Chose Movie ID:")
    print_projections(movie_id)
    pr_id = input("Chose projection ID: ")
    number_of_sits = input("How many sits you need: ")
    if is_enought_sits(number_of_sits, pr_id) is False:
        while is_enought_sits(number_of_sits, pr_id) is False:
            print("Not enoght sits left, you can buy less sits?")
            number_of_sits = input("You can exit(tipe: exit) or you can try with less sits: ")
    if number_of_sits == "exit":
        return number_of_sits
    sits = []
    chosed = []
    for index in range(int(number_of_sits)):
        print_sits(pr_id, chosed)
        sits.append([int(input("Chose row: "))])
        sits[index].append(int(input("Chose sit: ")))
        while is_the_sit_is_free(sits[index], pr_id) is False:
            print("This sit is already taken or invalid!!! Try again!")
            print_sits(pr_id, chosed)
            sits[index][0] = int(input("Chose row: "))
            sits[index][1] = int(input("Chose sit: "))
        chosed.append(sits[index])
    fin_print(movie_id, pr_id, chosed)
    command = input("For conform type 'fin', for exit without conforming type 'exit'")
    if command == "fin":
        for sit1 in sits:
            session.add(Reservation(projection_id=pr_id, username=user_name,
                                    row=sit1[0], sit=sit1[1]))
        session.commit()
    elif command == "exit":
        return False


def main():
    #print_sits(1, [[]])
    make_reservation()


if __name__ == '__main__':
    main()
