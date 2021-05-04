from os import O_TEMPORARY
from database import Database
from database_HighControls import HighControlDB
from user import User
from accounts import *

db = Database()


def reset():
    dbH = HighControlDB()
    dbH.resetDatabase()


def addNewUser():
    tempUser.newUser(123, "qwe", 'C', "NC", "Mark", "F",
                     "DC", 20, "M", "s", "b", "c", "ph")
    tempUser.newUser(345, "qwe", 'A', "NC", "Mork", "F",
                     "DC", 20, "M", "s", "b", "c", "ph")


def login():
    while (True):
        tempUser = User(db)

        mode = None
        user = None
        number = input("Phone Number: ")
        password = input("Password: ")

        if (tempUser.verifyUser(number, password)):
            mode = tempUser.getType()
            if (mode == 'C'):
                user = Customer(db)
            elif (mode == 'A'):
                user = Admin(db)
            else:
                print("Error")

            tempUser.transferInfoTo(user)
            del tempUser
        else:
            print("No Match!!!")
            break


def removing():
    tempUser = User(db)
    tempUser.verifyUser(123, 'qwe')
    tempUser.removeUser()
