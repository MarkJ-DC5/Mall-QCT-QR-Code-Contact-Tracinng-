from mysql.connector import optionfiles
from screen import Screen, system


class ScreenAdmin(Screen):
    def __init__(self, admin):
        Screen.__init__(self)
        super().__init__()
        self._admin = admin
        self.adminTracedContacts()

    def printTraced(self, traced, maxDepth=3, depth=0, detailedID=-1):
        if(depth <= maxDepth):
            for inf in traced:
                card = ""

                if(depth == 1):
                    level = "\t    "
                elif(depth == 2):
                    level = "\t\t   "
                elif(depth == 3):
                    level = "\t\t\t   "

                if(inf != detailedID):
                    info = self._admin.getCustSampleInfo(inf)
                    if(depth == 0):
                        dtRec = str(((self._admin._db.query(
                            "SELECT dt_rec FROM primary_infecteds WHERE inf_id = {} and dt_rem IS NULL".format(inf)))[0]).date())
                        card = "{0}{1:-^30}\n{0}| Date: {4:<20} {2:>1}\n{0}| Name: {5:<20} {2:>1} \n{0}{3:-^30}".format(
                            " ", " {} ".format(inf), "|", "", dtRec, info["name"])
                    elif(depth > 0):
                        card = "{0}{1:-^30}\n{0}| Name: {4:<20} {2:>1} \n{0}{3:-^30}".format(
                            level, " {} ".format(inf), "|", "", info["name"])
                else:
                    info = self._admin.getCustInfo(inf)
                    if(depth == 0):
                        dtRec = str(((self._admin._db.query(
                            "SELECT dt_rec FROM primary_infecteds WHERE inf_id = {} and dt_rem IS NULL".format(inf)))[0]).date())
                        card = "{0}{1:-^30}\n{0}| Date Recorded: {4:<30}\n{0}| Name: {5:<30}\n{0}| Phone Number: {6:<30}\n{0}| Age: {7:<30}\n{0}| Gener: {8:<30}\n{0}| Address:\n |\t{9:<30}\n{0}{3:-^30}".format(
                            " ", " {} ".format(inf), "|", "", dtRec, info["name"], info["cNum"], info["age"], info["gender"], info["address"])
                    elif(depth > 0):
                        card = "{0}{1:-^30}\n{0}| Name: {4:<20}\n{0}| Phone Number: {5:<20}\n{0}| Age: {6:<20}\n{0}| Gener: {7:<20}\n{0}| Address:\n {0}|\t{8:<20}\n{0}{3:-^30}".format(
                            level, " {} ".format(inf), "|", "", info["name"], info["cNum"], info["age"], info["gender"], info["address"])

                print(card, '\n')

                if(traced[inf] != None):
                    nextDepth = depth + 1
                    self.printTraced(
                        traced[inf], maxDepth, nextDepth, detailedID)

    def adminTracedContacts(self, focus=-1):
        self._admin.contact.startTracing()
        tracedContacts = (self._admin.contact.getTracedContact())[
            "byContactTrace"]
        system('cls')
        print("\n=============================================================\n")
        print("Traced Contact \n")
        print("Primaries \n")
        for traced in tracedContacts:
            self.printTraced(traced, detailedID=focus)
        print("\t{0:-^50}".format(" end "))

        print("")
        print("Options: ")
        print("\t f: Focus")
        print("\t m: Menu")
        print("\t e: Exit")
        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "f"):
            setFocus = input("Enter User's ID: ")
            if(self.isValidInt(setFocus, 1)):
                setFocus = int(setFocus)
                self.adminTracedContacts(setFocus)
            else:
                self.adminTracedContacts()
        elif(optToShow == "m"):
            self.adminMenu("Traced Contacts")
        elif(optToShow == "e"):
            return 0
        else:
            self.adminTracedContacts()

    def adminPendingProofs(self, rows=5):
        pendings = self._admin.getPendingProof(rows)
        system('cls')
        print("\n=============================================================\n")
        print("Pending Proofs \n")
        print("\t{0:>5}  {1:<20} {2:<20}".format("ReqID", "Req By", "Req On"))

        row = 1
        for que in pendings:
            name = (self._admin.getCustSampleInfo(que["uploadedBy"]))["name"]

            print("\t{0:>5}  {1:<20} {2:<20}".format(
                que["uploadedBy"], name, que["dtUploaded"]))
            row += 1

        print("\t{0:-^50}".format(" end "))

        print("")
        print("Options: ")
        print("\t v: View")
        print("\t s: Show More")
        print("\t m: Menu")
        print("\t e: Exit")
        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "v"):
            toView = input("ReqID to View: ")
            if (self.isValidInt(toView, 1)):
                toView = int(toView)
                for que in pendings:
                    if(que["uploadedBy"] == toView):
                        print("\t{0:>20}:   {1:<20}".format("pID", que["pID"]))
                        print("\t{0:>20}:   {1:<20}".format(
                            "Link to Proof", que["proofLink"]))
                        print("\t{0:>20}:   {1:<20}".format(
                            "Uploader ID", que["uploadedBy"]))
                        print("\t{0:>20}:   {1:<20}".format(
                            "Date Uploaded", que["dtUploaded"]))
                        print("\t{0:>20}:   {1:<20}".format(
                            "Status", que["status"]))

                        print("Sub Options: ")
                        print("\ta: Approve")
                        print("\td: Deny")
                        print("\tn: Nothing")
                        do = input("Do: ")

                        if(do == "a"):
                            self._admin.updateProofStat(
                                que["uploadedBy"], "Approved")
                        elif(do == "d"):
                            self._admin.updateProofStat(
                                que["uploadedBy"], "Denied")
                        self.adminPendingProofs()
                        break
            else:
                self.adminPendingProofs()
        elif(optToShow == "v"):
            rows += 5
            self.adminPendingProofs(rows)
        elif(optToShow == "m"):
            self.adminMenu("Pending Proofs")
        elif(optToShow == "e"):
            return 0
        else:
            self.adminPendingProofs()

    def adminGeneralInfo(self):
        self.Home(self._admin)
        self.adminMenu("General Info")

    def adminStores(self, rows=5):
        storeIDs = self._admin.getStoresID(rows)

        system('cls')
        print("\n=============================================================\n")
        print("Stores \n")

        print("{0:>8} {1:>5} {2:>3} {3:>6}  {4:<15} {5:<11}".format(
            "ID", "Num", "Flr", "Wing", "Name", "Phone"))
        for sID in storeIDs:
            storeInfo = self._admin.getStoreInfo(sID)
            print("{0:>8} {1:>5} {2:>3} {3:>6}  {4:<15} {5:<11}".format(
                storeInfo["sID"], storeInfo["sNum"], storeInfo["floor"], storeInfo["wing"], storeInfo["name"], storeInfo["cNum"]))

        print("")
        print("Options: ")
        print("\t s: Show More")
        print("\t g: Generate QR Code")
        print("\t a: Add New Store")
        print("\t d: Delete Store")
        print("\t m: Menu")
        print("\t e: Exit")
        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "s"):
            rows += 5
            self.adminStores(rows)

        elif(optToShow == "g"):
            toGenerate = input("Enter Store ID to generate QR Code: ")
            if(self.isValidInt(toGenerate, 1)):
                toGenerate = int(toGenerate)
                storeInfo = self._admin.getStoreInfo(toGenerate)
                path = self._admin.generateQRCode(storeInfo)
                if(path != False):
                    print("QR Code Generated and Saved in {}".format(path))
                else:
                    print("Error in Generating QR Code!")
                system('pause')
                self.adminStores(rows)
            else:
                self.adminStores(rows)

        elif(optToShow == "a"):
            storeNum = input("StoreNum: ")
            floor = input("Floor: ")
            wing = input("Wing: ")
            name = input("Name: ")
            cNum = input("Phone Number: ")
            email = input("Email: ")
            if(self.isValidInt(storeNum, 1) and self.isValidInt(floor, 1) and
                self.isValidString(wing) and wing in ["North", "South", "East", "West"] and
                    self.isValidString(name) and self.isValidCnum(cNum) and len(email) > 5):
                if(self._admin.newStore(storeNum, floor, wing, name, cNum, email)):
                    print("Store is Added...")
                else:
                    print("Deleted...")
                system('pause')
                self.adminStores(rows)
            else:
                print("One or More Inputs Invalid")
                system('pause')
                self.adminStores(rows)

        elif(optToShow == "d"):
            toDelete = input("Enter Store ID to Delete: ")
            if(self.isValidInt(toDelete, 1)):
                toDelete = int(toDelete)
                if(not self._admin.deleteStore(toDelete)):
                    system('pause')
                    self.adminStores(rows)

            else:
                self.adminStores(rows)
        elif(optToShow == "m"):
            self.adminMenu("Stores")
        elif(optToShow == "e"):
            return 0
        else:
            self.adminStores(rows)

    def adminAccount(self):
        info = self._admin.getInfo()
        info.pop('uID', None)
        info.pop('type', None)
        info.pop('infCov', None)
        info.pop('dtAdd', None)
        info.pop('dtRem', None)

        system('cls')
        print("\n===================================================================\n")
        print("Account:")

        for i in info:
            print('\t {:<10}: {:<20}'.format(i, str(info[i])))

        print("")
        print("Options: ")
        print("\t ed: Edit")
        print("\t a: Add New Admin")
        print("\t d: delete")
        print("\t m: Menu")
        print("\t e: Exit")

        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "ed"):
            keyRow = input("Row Name to edit: ")
            valueRow = input("New Value to edit: ")
            if(self.editInfo(self._admin, keyRow, valueRow)):
                self._admin.reloadInfo()
                print("Update Applied")
            self.adminAccount()

        elif(optToShow == "a"):
            cNum = input("Contact Number (09xxxxxxxxx, 11chars): ")
            passwd = input("Password (8chars): ")

            isValidCnum = self.isValidCnum(cNum)
            isValidPasswd = self.isValidPassword(passwd)

            if(isValidCnum and isValidPasswd):
                self.signUp(cNum, passwd, 'A')
            else:
                print("Contact number format is {} and \nPassword format is {}".format(
                    isValidCnum, isValidPasswd))
                system('pause')
                self.adminAccount()

        elif(optToShow == "d"):
            isSure = input(
                "If you delete your account, \nyou will no longer have access to this. \nAre you sure you want to delete? y/n")
            if(isSure == 'y'):
                self._admin.deleteAccount()
                print("GoodBye!")
                system('pause')
                return 0
        elif(optToShow == "m"):
            self.adminMenu("Account Info")
        elif(optToShow == "e"):
            return 0
        else:
            self.adminAccount()

    def adminMenu(self, prevPage):
        pages = {"t": "Traced Contacts", "p": "Pending Proofs",
                 "g": "General Info", "s": "Stores", "a": "Account"}

        pages = {key: val for key, val in pages.items() if val != prevPage}

        print("Here's Your Menu: ")
        for key in pages.keys():
            print("\t {}: {}".format(key, pages[key]))
        print("\t e: exit")

        choosen = input("Menu to open: ")
        if(choosen == "t"):
            self.adminTracedContacts()
        elif(choosen == "p"):
            self.adminPendingProofs()
        elif(choosen == "g"):
            self.adminGeneralInfo()
        elif(choosen == "s"):
            self.adminStores()
        elif(choosen == "a"):
            self.adminAccount()
        elif(choosen == "e"):
            return 0
        else:
            self.adminMenu(prevPage)
