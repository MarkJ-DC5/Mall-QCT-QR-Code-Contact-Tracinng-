from user import User
from database import Database
from accounts import Customer, Admin
from menuCustomer import *
from menuAdmin import *
from os import O_APPEND, stat_result, system


def isValidString(value, withSpace=True):
    if(len(value) > 3):
        if(withSpace):
            if all(x.isalpha() or x.isspace() for x in value):
                return True
            else:
                return False
        else:
            if all(x.isalpha() for x in value):
                return True
            else:
                return False
    else:
        return False


def isValidInt(value):
    numbersSTR = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    if(len(value) >= 2):
        for i in value:
            if (i not in numbersSTR or i == ' '):
                return False
        return True
    else:
        return False


def signUp(user, cNum, passwd, mode='C'):
    toPrint = ["===================================================================\n",
               "Sign Up: ",
               "-------------------------------------------------------------------",
               "Enter 'exit' to Exit",
               "Contact Number: {}".format(cNum),
               "Password: {}".format(passwd)]

    if(mode == 'C'):
        toPrint.append("Type: C")
    elif(mode == 'A'):
        toPrint.append("Type: A")

    countedInputs = 6
    system('cls')
    for p in toPrint:
        print(p)

    while True:
        if countedInputs == 6:
            fName = input("First name: ")
            if(fName == 'exit'):
                break
            if(isValidString(fName)):
                toPrint.append("First name: {}".format(fName))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 7:
            lName = input("Last name: ")
            if(lName == 'exit'):
                break

            if(isValidString(lName)):
                toPrint.append("Last name: {}".format(lName))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 8:
            age = input("Age: ")
            if(age == 'exit'):
                break

            if(isValidInt(age)):
                if(int(age) > 18 and int(age) < 90):
                    toPrint.append("Age: {}".format(age))
                    countedInputs += 1
                else:
                    system('cls')
                    for p in toPrint:
                        print(p)
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 9:
            gender = input("Gender: ")
            if(gender == 'exit'):
                break

            if(gender == "Male" or gender == "Female" or gender == "Other"):
                toPrint.append("Gender: {}".format(gender))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 10:
            street = input("Street: ")
            if(street == 'exit'):
                break

            if(len(street) > 3):
                toPrint.append("Street: {}".format(street))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 11:
            barangay = input("Barangay: ")
            if(barangay == 'exit'):
                break

            if(isValidString(street)):
                toPrint.append("Barangay: {}".format(barangay))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 12:
            city = input("City: ")
            if(city == 'exit'):
                break

            if(isValidString(city)):
                toPrint.append("City: {}".format(city))
                countedInputs += 1
            else:
                system('cls')
                for p in toPrint:
                    print(p)

        elif countedInputs == 13:
            user.newUser(cNum, passwd, 'C',
                         fName, lName, age, gender,
                         street, barangay, city)
            return

    print("Thank You for Using \nQR Code Mall Contact Tracing!")
    # age = input("Age: ")
    # gender = input("Gender (Male, Female, Other): ")
    # fname = input("Street: ")
    # fname = input("Barangay: ")
    # fname = input("City: ")
    # p_cNum, p_passwd, p_type,
    # p_fName, p_lName, p_age, p_gender,
    # p_street, p_barangay, p_city
    # pass


def logIn(user):
    attempts = 3

    while attempts > 0:
        system('cls')
        print("====== QR Code Mall Contact Tracing =====", '\n')
        cNum = "09101010101"
        passwd = "TheMarker"
        # cNum = input("Contact Number (09xxxxxxxxx, 11chars): ")
        # passwd = input("Password (8chars): ")
        print('')

        cNumLen = len(cNum)
        passwdLen = len(passwd)
        isCNumValid = None
        isPasswdValid = None

        if(cNumLen == 11 and cNum[0] == "0" and cNum[1] == "9"):
            isCNumValid = isValidInt(cNum)

        else:
            isCNumValid = False

        if(passwdLen >= 8):
            isPasswdValid = True
            for i in passwd:
                if(i == ' '):
                    isPasswdValid = False
        else:
            isPasswdValid = False

        if(isCNumValid and isPasswdValid):
            if(user.verifyUser(cNum, passwd)):
                return user.getUserType()
            else:
                print("No Credential Matched: {} attemps left".format(attempts - 1))
                print("r: Retry")
                print("c: Create New Account")
                print("e: Exit")
                choosenOpt = input("Do: ")

                if(choosenOpt == "r"):
                    print('\n')
                    continue
                elif(choosenOpt == "c"):
                    signUp(user, cNum, passwd)
                    user.verifyUser(cNum, passwd)
                    return user.getUserType()
                elif(choosenOpt == "e"):
                    return 0
                else:
                    print('Invalid Input!')
                    system('pause')
                attempts -= 1
            print('\n')

            print("To Many Attemps\n")
        else:
            print("Contact number format is {} and \nPassword format is {}".format(
                isCNumValid, isPasswdValid))
            system('pause')
    return False


def customerHome(customer):
    custInfo = customer.getCompactInfo()
    storesHighCount = customer.getStoreWithHighCount()
    numOfHigh = len(storesHighCount)
    storesLowCount = customer.getStoreWithLowCount()
    numOfLow = len(storesLowCount)

    system('cls')
    print("\n===================================================================\n")
    print("Good Day, {}!".format(custInfo["name"]))
    print("You're current Health Status is {}".format(custInfo["infCov"]))
    print("The total customer entered in the mall is {} \n".format(
        customer.countEntered()))

    print("-------------------------------------------------------------------\n")
    print("Top {} store with the Highest Total Customer: \n".format(numOfHigh))
    for store in storesHighCount:
        print("\t Name: {}".format(store["store"]["name"]))
        print("\t Count: {}".format(store["count"]))
        store = store["store"]
        print("\t Location: store #: {} | floor: {} | wing: {} \n".format(
            store["sNum"], store["floor"], store["wing"]))

    print('\n')

    print("Top {} store with the Lowest Total Customer: \n".format(numOfLow))
    for store in storesLowCount:
        print("\t Name: {}".format(store["store"]["name"]))
        print("\t Count: {}".format(store["count"]))
        store = store["store"]
        print("\t Location: store #: {} | floor: {} | wing: {} \n".format(
            store["sNum"], store["floor"], store["wing"]))
    print("===================================================================\n")

    customerMenu(customer, "Home")


def customerHistory(customer, detailedRow=-1):
    history = customer.getHistory()

    system('cls')
    print("\n===================================================================\n")
    print("Dates Entered: ")

    if(history != False):
        entryCount = 1
        for entry in history:
            print('\t', entryCount, "|", entry['date'])
            print("\t---------------------")

            if(detailedRow == entryCount):
                for store in entry['stores']:
                    print("\t\tName: {}".format(store["name"]))
                    print("\t\tLocation: ")
                    print("\t\t     store #: {} | floor: {} | wing: {}".format(
                        store["sNum"], store["floor"], store["wing"]))
                    print("\t\tTime: {} \n".format(store["timeEnt"]))
            entryCount += 1

        print("===================================================================\n")

        print("")
        print("Options: ")
        print("\t s: Show store")
        print("\t m: Menu")
        print("\t e: Exit")
        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "s"):
            toView = int(
                input("Enter row of corresponding \ndate to view visited store: "))
            customerHistory(customer, toView)
        elif(optToShow == "m"):
            customerMenu(customer, "History")
        elif(optToShow == "e"):
            return 0
        else:
            customerHistory(customer)
    else:
        print("\nYou haven't entered the mall with the app\n")
        customerMenu(customer, "History")


def customerChangeHealth(customer):
    system('cls')
    print("\n===================================================================\n")
    print("Are you infected?")
    proofLink = input("link to medical proof or x to cancel: ")

    if (proofLink != "x"):
        if(customer.uploadProof(proofLink) == True):
            print(
                "Proof is now on 'Pending' status. Once \napproved your health status will automatically update")

    print('')
    customerMenu(customer, "Change Health Status")


def editInfo(customer, key, value):
    forbidden = ["infCov", "dtAdd"]
    intType = ["cNum", "age"]
    strType = ["fName", "lName", "gender", "street", "barangay", "city"]

    if(key in forbidden):
        print("Not allowed to change")
        system('pause')
        return False

    elif(key in intType):
        if(isValidInt(value)):
            if(key == "cNum"):
                if(len(value) == 11 and value[0] == "0" and value[1] == "9"):
                    customer.updateInfo(["c_num"], [value])
                else:
                    print("Invalid Value")
                    system('pause')
                    return False

            elif(key == "age"):
                if(int(value) > 18 and int(value) < 90):
                    customer.updateInfo(["age"], [value])
                else:
                    print("Invalid Value")
                    system('pause')
                    return False

            return True
        else:
            print("Invalid Value")
            system('pause')
            return False

    elif(key in strType):
        if(isValidString(value)):
            if(key == "fName"):
                customer.updateInfo(["f_name"], [value])
            elif(key == "lName"):
                customer.updateInfo(["l_name"], [value])

            elif(key == "gender"):
                if(value in ["Male", "Female", "Other"]):
                    customer.updateInfo(["gender"], [value])
                else:
                    print("Invalid Value")
                    system('pause')
                    return False

            elif(key == "street"):
                customer.updateInfo(["street"], [value])
            elif(key == "barangay"):
                customer.updateInfo(["barangay"], [value])
            elif(key == "city"):
                customer.updateInfo(["city"], [value])
            return True
        else:
            print("Invalid Value")
            system('pause')
            return False
    elif(key == "passwd"):
        if(len(value) >= 8 and " " not in value):
            customer.updateInfo(["passwd"], [value])
            return True
        else:
            print("Invalid Value")
            system('pause')
            return False

    print("Not a Row Name!")
    system('pause')
    return False


def customerAccount(customer):
    info = customer.getExpandedInfo()
    info.pop('type', None)

    system('cls')
    print("\n===================================================================\n")
    print("Account:")

    for i in info:
        print('\t {:<10}: {:<20}'.format(i, str(info[i])))

    print("")
    print("Options: ")
    print("\t ed: Edit")
    print("\t m: Menu")
    print("\t e: Exit")

    optToShow = input("Opt To Show: ")
    print("")

    if(optToShow == "ed"):
        keyRow = input("Row Name to edit: ")
        valueRow = input("New Value to edit: ")
        if(editInfo(customer, keyRow, valueRow)):
            customer.reloadInfo()
            print("Update Applied")
        customerAccount(customer)
    elif(optToShow == "m"):
        customerMenu(customer, "Account Info")
    elif(optToShow == "e"):
        return 0
    else:
        customerAccount(customer)


def customerMenu(customer, prevPage):
    pages = {"hm": "Home", "hs": "History",
             "c": "Change Health Status", "a": "Account Info"}
    pages = {key: val for key, val in pages.items() if val != prevPage}

    print("Here's Your Menu: ")
    for key in pages.keys():
        print("\t {}: {}".format(key, pages[key]))
    print("\t e: exit")

    choosen = input("Menu to open: ")
    if(choosen == "hm"):
        customerHome(customer)
    elif(choosen == "hs"):
        customerHistory(customer)
    elif(choosen == "c"):
        customerChangeHealth(customer)
    elif(choosen == "a"):
        customerAccount(customer)
    elif(choosen == "e"):
        return 0
    else:
        customerMenu(customer, prevPage)
    # customerHome(customer)


def adminHome(admin):
    system('cls')
    print("Admin")


def main():
    system('cls')

    db = Database()
    tempUser = User(db)
    userType = logIn(tempUser)

    if userType == 'C':
        customer = Customer(db)
        tempUser.transferInfoTo(customer)
        del tempUser
        customerHome(customer)
    elif userType == 'A':
        admin = Admin(db)
        tempUser.transferInfoTo(admin)
        del tempUser
        adminHome(admin)
    else:
        return 0


if __name__ == "__main__":
    main()
