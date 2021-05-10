from os import O_APPEND, stat_result, system


class Screen():
    def __init__(self, user=None) -> None:
        self.__user = user

    def setUser(self, user):
        self.__user = user

    def isValidString(self, value, withSpace=True):
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

    def isValidInt(self, value, minChar=2):
        numbersSTR = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        if(len(value) >= minChar):
            for i in value:
                if (i not in numbersSTR or i == ' '):
                    return False
            return True
        else:
            return False

    def isValidAge(self, age):
        if(self.isValidInt(age)):
            if(int(age) > 18 and int(age) < 90):
                return True
        return False

    def isValidGender(self, gender):
        if(gender in ["Male", "Female", "Other"]):
            return True
        return False

    def isValidCnum(self, cNum):
        if(len(cNum) == 11 and cNum[0] == "0" and cNum[1] == "9"):
            if(self.isValidInt(cNum)):
                return True
        return False

    def isValidPassword(self, passwd):
        if(len(passwd) >= 8 and " " not in passwd):
            return True
        else:
            return False

    def editInfo(self, user, key, value):
        forbidden = ["infCov", "dtAdd"]
        intType = ["cNum", "age"]
        strType = ["fName", "lName", "gender", "street", "barangay", "city"]

        if(key in forbidden):
            print("Not allowed to change")
            system('pause')
            return False

        elif(key in intType):
            if(self.isValidInt(value)):
                if(key == "cNum"):
                    if(self.isValidCnum(value)):
                        user.updateInfo(["c_num"], [value])
                    else:
                        print("Invalid Value")
                        system('pause')
                        return False

                elif(key == "age"):
                    if(self.isValidAge(value)):
                        user.updateInfo(["age"], [value])
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
            if(self.isValidString(value)):
                if(key == "fName"):
                    user.updateInfo(["f_name"], [value])
                elif(key == "lName"):
                    user.updateInfo(["l_name"], [value])

                elif(key == "gender"):
                    if(self.isValidGender(value)):
                        user.updateInfo(["gender"], [value])
                    else:
                        print("Invalid Value")
                        system('pause')
                        return False

                elif(key == "street"):
                    user.updateInfo(["street"], [value])
                elif(key == "barangay"):
                    user.updateInfo(["barangay"], [value])
                elif(key == "city"):
                    user.updateInfo(["city"], [value])
                return True
            else:
                print("Invalid Value")
                system('pause')
                return False
        elif(key == "passwd"):
            if(self.isValidPassword()):
                user.updateInfo(["passwd"], [value])
                return True
            else:
                print("Invalid Value")
                system('pause')
                return False

        print("Not a Row Name!")
        system('pause')
        return False

    def signUp(self, cNum, passwd, mode='C'):
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
                fName = input("First name: ".format())
                if(fName == 'exit'):
                    break
                if(self.isValidString(fName)):
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

                if(self.isValidString(lName)):
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

                if(self.isValidAge(age)):
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

                if(self.isValidGender(gender)):
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

                if(len(barangay) > 3):
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

                if(len(city) > 3):
                    toPrint.append("City: {}".format(city))
                    countedInputs += 1
                else:
                    system('cls')
                    for p in toPrint:
                        print(p)

            elif countedInputs == 13:
                self.__user.newUser(cNum, passwd, mode,
                                    fName, lName, age, gender,
                                    street, barangay, city)
                return

        print("Thank You for Using \nQR Code Mall Contact Tracing!")

    def Home(self, user):
        custInfo = user.getCompactInfo()
        storesHighCount = user.getStoreWithHighCount()
        numOfHigh = len(storesHighCount)
        storesLowCount = user.getStoreWithLowCount()
        numOfLow = len(storesLowCount)

        system('cls')
        print("\n===================================================================\n")
        print("Good Day, {}!".format(custInfo["name"]))
        print("You're current Health Status is {}".format(custInfo["infCov"]))
        print("The total customer entered in the mall is {} \n".format(
            user.countEntered()))

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

    def logIn(self):
        attempts = 3

        while attempts > 0:
            system('cls')
            print("====== QR Code Mall Contact Tracing =====", '\n')
            cNum = input("Contact Number (09xxxxxxxxx, 11chars): ")
            passwd = input("Password (8chars): ")
            print('')

            isValidCnum = self.isValidCnum(cNum)
            isValidPasswd = self.isValidPassword(passwd)

            if(isValidCnum and isValidPasswd):
                if(self.__user.verifyUser(cNum, passwd)):
                    return self.__user.getUserType()
                else:
                    print("No Credential Matched: {} attemps left".format(
                        attempts - 1))
                    print("r: Retry")
                    print("c: Create New Account")
                    print("e: Exit")
                    choosenOpt = input("Do: ")

                    if(choosenOpt == "r"):
                        print('\n')
                        continue
                    elif(choosenOpt == "c"):
                        self.signUp(cNum, passwd)
                        self.__user.verifyUser(cNum, passwd)
                        return self.__user.getUserType()
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
                    isValidCnum, isValidPasswd))
                system('pause')
        return False
