from os import O_TEMPORARY, read, write

import names
from accounts import *
from database import Database, random
from database_HighControls import HighControlDB
from user import User
from contact import Contact

db = HighControlDB()


def reset():
    db.resetDatabase()


def addNewUser():
    tempUser = User(db)
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
            mode = tempUser.getUserType()
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
    tempUser.verifyUser("09001", 'passwd')
    tempUser.removeUser()


def addStores():
    storesData = [[1, 1, "North",	"Ace Hardware", "0918", "store@email.com", str(datetime.now().date())],
                  [2, 1, "North",	"Jollibee", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [3, 1, "North",	"Mcdo", "0918", "store@email.com",
                      str(datetime.now().date())],
                  [4, 1, "North",	"Kripy Kreme", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [5, 1, "South",	"Bench", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [6, 1, "South",	"Miniso", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [7, 1, "South",	"Greenich", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [8, 1, "South",	"Pizza Hut", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [9, 2, "West",	"Pancake House", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [10, 2,	"West", "Penshoppe", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [11, 2,	"West", "Burger King", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [12, 2,	"East", "Subway", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [13, 2,	"East", "JCO", "0918", "store@email.com",
                      str(datetime.now().date())],
                  [14, 2,	"East", "Starbuck", "0918",
                      "store@email.com", str(datetime.now().date())],
                  [15, 2, "East", "Dairy Quenn", "0918", "store@email.com", str(datetime.now().date())]]

    for row in storesData:
        # print(row)
        db.insert("stores", ["store_num", "floor", "wing",
                             "name", "c_num", "email", "dt_add"], row)


def addManyNewUSers(count):
    tempUser = User(db)
    cNumber = 9000
    added = 0
    while added < count:
        cNumber += 1
        strCNum = "0" + str(cNumber)
        added += 1
        fname = names.get_first_name()
        lname = names.get_last_name()
        age = random.randint(18, 40)
        if (random.randint(0, 1) == 1):
            sex = 'Male'
        else:
            sex = 'Female'
        # print(strCNum, fname, lname, age, sex)
        tempUser.newUser(strCNum, "passwd", 'C', fname,
                         lname, age, sex, "street", "barangay", "city")

    tempUser.newUser("1111", "qwer", 'A', "Mark", "Cruz",
                     20, "Male", "street", "barangay", "city")


def GenerateQR(storeNum):
    adminUser = Admin(db)
    adminUser.verifyUser("1111", "qwer")
    tempStore = adminUser.getStoreInfo(storeNum)
    print(tempStore)
    if (input("Is right? Y/N ") == "Y"):
        adminUser.generateQRCode(tempStore)
    else:
        print("Abort!!!")


def ReadQR():
    cust = Customer(db)
    cust.verifyUser("09002", "passwd")
    cust.readQR("QRcodes/4_4_Kripy Kreme.jpg")


def customerTest():
    cust = Customer(db)
    cust.verifyUser("09001", "passwd")
    # print(cust.getInfo())
    print(cust.countEntered())
    # print(cust.getStoreWithHighCount())
    # print(cust.getStoreWithLowCount())
    # cust.getHistory()
    # cust.uploadProof("link to something")
    # cust.updateHealthStatus()
    # cust.updateInfo(["u_id", "c_num", "passwd", "type", "inf_cov", "f_name", "l_name", "age", "gender", "street", "barangay", "city", "dt_add", "dt_rem"], [
    #                 110, "1234", "qwert", "A", "Healthy", "Monica", "Geller", 30, "Female", "s", "b", "c", str(datetime.now()), str(datetime.now())])


def adminTest():
    admin = Admin(db)
    admin.verifyUser("1111", "qwer")
    print(admin.getPendingProof())
    # admin.deleteAccount()
    # admin.deleteStore(1)
    # admin.updateProofStat(1, 'Approved')
    # admin.newStore(20, 2, "West", "Something", "0900", "@email.com")
    # admin.getStores()


def contactTrace():
    # db.createPrimeInfected()
    ct = Contact(db)
    print(ct.getTracedContact())
    # ct.updateTracedDB()


contactTrace()
