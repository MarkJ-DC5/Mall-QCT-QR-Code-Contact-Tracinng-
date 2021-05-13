from screen import Screen, system


class ScreenCustomer(Screen):
    def __init__(self, customer):
        Screen.__init__(self)
        super().__init__()
        self._customer = customer
        self.customerHome()

    def customerHome(self):
        self.Home(self._customer)
        self.customerMenu("Home")

    def customerHistory(self, detailedRow=-1, rows=5):
        history = self._customer.getHistory(rows)

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
            print("\t sm: Show More")
            print("\t m: Menu")
            print("\t e: Exit")
            optToShow = input("Opt To Show: ")
            print("")

            if(optToShow == "s"):
                toView = int(
                    input("Enter row of corresponding \ndate to view visited store: "))
                self.customerHistory(toView, rows)
            elif(optToShow == "sm"):
                Newrows = rows + 5
                self.customerHistory(rows=Newrows)
            elif(optToShow == "m"):
                self.customerMenu("History")
            elif(optToShow == "e"):
                return 0
            else:
                self.customerHistory(rows)
        else:
            print("\nYou haven't entered the mall with the app\n")
            self.customerMenu("History")

    def customerChangeHealth(self):
        system('cls')
        print("\n===================================================================\n")
        print("Are you infected?")
        proofLink = input("link to medical proof or x to cancel: ")

        if (proofLink != "x"):
            if(self._customer.uploadProof(proofLink) == True):
                print(
                    "Proof is now on 'Pending' status. Once \napproved your health status will automatically update")

        print('')
        self.customerMenu("Change Health Status")

    def customerAccount(self):
        info = self._customer.getInfo()
        info.pop('u_id', None)
        info.pop('type', None)
        info.pop('inf_cov', None)
        info.pop('dt_add', None)
        info.pop('dt_rem', None)

        system('cls')
        print("\n===================================================================\n")
        print("Account:")

        for i in info:
            print('\t {:<10}: {:<20}'.format(i, str(info[i])))

        print("")
        print("Options: ")
        print("\t ed: Edit")
        print("\t d: delete")
        print("\t m: Menu")
        print("\t e: Exit")

        optToShow = input("Opt To Show: ")
        print("")

        if(optToShow == "ed"):
            keyRow = input("Row Name to edit: ")
            valueRow = input("New Value to edit: ")
            if(self.editInfo(self._customer, keyRow, valueRow)):
                self._customer.reloadInfo()
                print("Update Applied")
            self.customerAccount()
        elif(optToShow == "d"):
            isSure = input(
                "If you delete your account, \nyou will no longer have access to this. \nAre you sure you want to delete? y/n")
            if(isSure == 'y'):
                self._customer.deleteAccount()
                print("GoodBye!")
                system('pause')
                return 0
        elif(optToShow == "m"):
            self.customerMenu("Account Info")
        elif(optToShow == "e"):
            return 0
        else:
            self.customerAccount()

    def customerMenu(self, prevPage):
        pages = {"s": "Scan", "hm": "Home", "hs": "History",
                 "c": "Change Health Status", "a": "Account Info"}
        pages = {key: val for key, val in pages.items() if val != prevPage}

        print("Here's Your Menu: ")
        for key in pages.keys():
            print("\t {}: {}".format(key, pages[key]))
        print("\t e: exit")

        choosen = input("Menu to open: ")
        if(choosen == "s"):
            self._customer.scanQRCode()
            self.customerHome()
        elif(choosen == "hm"):
            self.customerHome()
        elif(choosen == "hs"):
            self.customerHistory()
        elif(choosen == "c"):
            self.customerChangeHealth()
        elif(choosen == "a"):
            self.customerAccount()
        elif(choosen == "e"):
            return 0
        else:
            self.customerMenu(prevPage)
