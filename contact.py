from database_HighControls import HighControlDB
from database import Database, random
from datetime import datetime, timedelta


class Contact():
    def __init__(self, database, depth=3):
        self.__db = database
        self.__primaryInfecteds = []
        self.__Traces = []

        # start tracing on construct
        self.__primaryInfecteds = self.getPrimaryInfecteds()
        self.__Traces = self.multipleTrace(self.__primaryInfecteds)

        # # self.__primeInfected = infID
        # self.__primeInfected = None
        # self.__db = database
        # self.__maxDepth = depth
        # # self.__dateEntered = self.__setDateEntered()
        # self.__dateEntered = None
        # self.__unordInfPerson = [self.__primeInfected]
        # self.__unordInfStores = []

        # self.__ordInfPerson = {}    # {'55': {24: None}}
        # self.__ordInfPerson[self.__primeInfected] = None
        # # self.__trace(self.__ordInfPerson, self.__dateEntered)

    def getPrimaryInfecteds(self):
        primaryInfectees = self.__db.query(
            "SELECT u_id FROM users WHERE inf_cov = 'Primary Inf' and dt_rem IS NULL")

        infecteesCount = len(primaryInfectees)
        if(infecteesCount == 1):
            self.__primaryInfecteds.append(primaryInfectees[0])
        elif(infecteesCount > 1):
            for i, tup in enumerate(primaryInfectees):
                primaryInfectees[i] = tup[0]
            self.__primaryInfecteds.append(primaryInfectees)

        return primaryInfectees

    def getDTEntered(self, uID):
        dtEntered = self.__db.query(
            "SELECT dt_rec FROM customers_health_record  WHERE u_id = {}  ORDER BY dt_rec DESC LIMIT 1".format(uID))

        if(len(dtEntered) > 0):
            dtEntered = dtEntered[0]
            return dtEntered

    def __cleanOutputList(self, srcList, refList):
        cleaned = []

        if(len(srcList) > 0):
            # from tuples to arrays
            if (len(srcList) > 1):
                for id in srcList:
                    cleaned.append(id[0])
            elif (len(srcList) == 1):
                cleaned.append(srcList[0])

            # removes repeated ID
            cleaned = list(dict.fromkeys(cleaned))

            # removes already recorded ID
            if (len(cleaned) > 0):
                for id in cleaned:
                    if (id in refList):
                        del cleaned[cleaned.index(id)]

        return cleaned

    def __addOneHr(self, datetime):
        newDT = datetime + timedelta(hours=1)
        return newDT

    def __getInfStores(self, infPerson, dtEnt, histInfStores):
        # get the list of stores visited
        infStores = self.__db.query(
            "SELECT s_id FROM customers_health_record WHERE u_id = {} AND dt_rec >= '{}'".format(
                infPerson, str(dtEnt)))

        # removes any form of repition from the result
        infStores = self.__cleanOutputList(infStores, histInfStores)

        # updte history of recorded
        histInfStores += infStores

        return infStores

    def __getInfectees(self, infector, infStore, dtEntMall, histInfPers):
        # get the time the infector entered the store
        dtEnt = self.__db.query("SELECT dt_rec FROM customers_health_record WHERE u_id = {} AND s_id = {} and dt_rec >= '{}' ORDER BY dt_rec ASC".format(
            infector, infStore, dtEntMall))
        infPersons = []

        if(len(dtEnt) == 1):
            dtEnt = dtEnt[0]

            # get the list of infected person
            infPersons = self.__db.query(
                "SELECT u_id FROM customers_health_record WHERE s_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infStore, str(dtEnt), str(self.__addOneHr(dtEnt))))

            # removes any form of repition from the result
            infPersons = self.__cleanOutputList(
                infPersons, histInfPers)

        elif (len(dtEnt) > 1):
            for dt in dtEnt:
                dt = dt[0]
                # get the list of infected person
                tempInfPersons = self.__db.query(
                    "SELECT u_id FROM customers_health_record WHERE s_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infStore, str(dt), str(self.__addOneHr(dt))))

                # removes any form of repition from the result
                tempInfPersons = self.__cleanOutputList(
                    tempInfPersons, histInfPers)

                infPersons.extend(tempInfPersons)
            dtEnt = dtEnt[0][0]

        # updte history of recorded
        histInfPers += infPersons

        # returns the list of infected people and time the infectore entered the shop
        return {"infecteds": infPersons, "dtEnt": dtEnt}

    def __trace(self, ordInfPerson, initalDT, histInfPers, histInfStores, currentDepth=0, maxDepth=3):
        # set the limit for the depth of recursing
        if (currentDepth < maxDepth):
            # perform tracing for every key in the dictionary of contacts
            for infector in ordInfPerson:
                if (initalDT != None):
                    stores = self.__getInfStores(
                        infector, initalDT, histInfStores)

                    # create a dictionary of people contacted by the infector
                    infectorContacts = {}
                    for store in stores:
                        infectees = self.__getInfectees(
                            infector, store, initalDT, histInfPers)

                        # fills the list of contacted person
                        for infected in infectees["infecteds"]:
                            infectorContacts[infected] = None

                    # the dictority for the contacted people is then set as the value for of the infector key
                    if (len(infectorContacts) > 0):
                        ordInfPerson[infector] = infectorContacts
                        currentDepth += 1
                        self.__trace(infectorContacts,
                                     infectees["dtEnt"], histInfPers, histInfStores, currentDepth)

                    elif (len(infectorContacts) == 0):
                        ordInfPerson[infector] = None

    def singleTrace(self, primaryInf):
        traced = {}
        traced[primaryInf] = None
        dtEnt = self.getDTEntered(primaryInf)
        histInfecteds = []
        hsitInfectedStores = []
        self.__trace(traced, dtEnt, histInfecteds, hsitInfectedStores)
        return traced

    def multipleTrace(self, primaryInfectees):
        traces = []
        for primeInf in primaryInfectees:
            dtEnt = self.getDTEntered(primeInf)
            trace = self.singleTrace(primeInf)
            traces.append(trace)

        return traces

    def getTracedContact(self):
        return self.__Traces


db = HighControlDB("f", fileName="dbTestCred.txt")


def resetCustHlthRec():
    db.query("DROP TABLE IF EXISTS Customers_Health_Record")
    db.query("CREATE TABLE Customers_Health_Record (\
        u_id int,\
        s_id int,\
        dt_rec datetime NOT NULL)")
    print("Customers_Health_Record Table Created")


def fillCCustHlthRec(intances=100, people=100, stores=15, timeDif=24):
    currentDT = datetime.now().replace(microsecond=0)
    # currentTimeInc = datetime.now().replace(microsecond=0) + timedelta(hours=1)
    print("Current Time: ", currentDT)

    i = 0
    while i < intances:
        operator = random.randint(0, 1)
        if (operator == 0):
            randDT = currentDT - \
                timedelta(hours=random.randint(0, timeDif))
        else:
            randDT = currentDT + \
                timedelta(hours=random.randint(0, timeDif))

        operator = random.randint(0, 1)
        if (operator == 0):
            randDT -= timedelta(minutes=random.randint(0, 50))
        else:
            randDT += timedelta(minutes=random.randint(0, 50))

        uID = random.randint(1, people)
        sID = random.randint(1, stores)

        recent = db.query("SELECT COUNT(u_id) FROM customers_health_record WHERE s_id = {} AND u_id = {} AND dt_rec BETWEEN \"{}\" and \"{}\"".format(
            uID, sID, str(randDT - timedelta(hours=1)), str(randDT)))
        recent = recent[0]

        if (recent == 0):
            db.insert("customers_health_record ", ["u_id", "s_id", "dt_rec"], [
                uID, sID, str(randDT)])
        else:
            print("Recent Entr Already Exist")

        i += 1


# resetCustHlthRec()
# fillCCustHlthRec(intances=2500, people=100, timeDif=72)
# instances directly
# people inversely
# timedef inversely

# i = 1
# while i <= 100:
#     id = i
#     ct = Contact(db)
#     print(ct.singleTrace(id, ct.getDTEntered(id)))
#     i += 1

# ct = Contact(db)
# print(ct.getTracedContact())
