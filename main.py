from os import O_APPEND, stat_result, system

from accounts import Admin, Customer
from database import Database
from screen import Screen
from screenAdmin import ScreenAdmin
from screenCustomer import ScreenCustomer
from user import User


def main():
    system('cls')

    db = Database()
    tempUser = User(db)
    screen = Screen(database=db)
    screen.setUser(tempUser)
    userType = screen.logIn()
    if userType == 'C':
        customer = Customer(db)
        tempUser.transferInfoTo(customer)
        del tempUser
        screenCustomer = ScreenCustomer(customer)
    elif userType == 'A':
        admin = Admin(db)
        tempUser.transferInfoTo(admin)
        del tempUser
        screenAdmin = ScreenAdmin(admin)
    else:
        return 0


if __name__ == "__main__":
    main()
