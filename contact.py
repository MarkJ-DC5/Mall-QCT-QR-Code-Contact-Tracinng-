from database_HighControls import HighControlDB
from database import Database, random
from datetime import datetime, timedelta


class Contact():
    def __init__(self, infID, database, depth=3):
        self.__primeInfected = infID
        self.__db = database
        self.__maxDepth = depth
        self.__dateEntered = None
        self.__unordInfPerson = [self.__primeInfected]
        self.__unordInfStores = []

        self.__ordInfPerson = {}    # {'55': {24: None}}
        self.__ordInfPerson[self.__primeInfected] = None

    def setDateEntered(self):
        self.__dateEntered = self.__db.query(
            "SELECT dt_rec FROM customers_health_record  WHERE u_id = {}  ORDER BY dt_rec ASC LIMIT 1".format(self.__primeInfected))

        if(len(self.__dateEntered) > 0):
            self.__dateEntered = self.__dateEntered[0]
            return self.__dateEntered

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

    def getInfStores(self, infPerson, dtEnt):
        # get the list of stores visited
        infStores = self.__db.query(
            "SELECT s_id FROM customers_health_record WHERE u_id = {} AND dt_rec >= '{}'".format(
                infPerson, str(dtEnt)))

        # removes any form of repition from the result
        infStores = self.__cleanOutputList(infStores, self.__unordInfStores)

        # updte history of recorded
        self.__unordInfStores += infStores

        return infStores

    def getInfectees(self, infector, infStore, dtEntMall):
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
                infPersons, self.__unordInfPerson)

        elif (len(dtEnt) > 1):
            for dt in dtEnt:
                dt = dt[0]
                # get the list of infected person
                tempInfPersons = self.__db.query(
                    "SELECT u_id FROM customers_health_record WHERE s_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infStore, str(dt), str(self.__addOneHr(dt))))

                # removes any form of repition from the result
                tempInfPersons = self.__cleanOutputList(
                    tempInfPersons, self.__unordInfPerson)

                infPersons.extend(tempInfPersons)
        # updte history of recorded
        self.__unordInfPerson += infPersons

        # returns the list of infected people and time the infectore entered the shop

        return {"infecteds": infPersons, "dtEnt": dtEnt}

    def trace(self, infector, initalDT, currentDepth=0):
        if (initalDT != None):
            stores = self.getInfStores(infector, initalDT)

            if(len(stores) > 0):
                for store in stores:
                    infectees = self.getInfectees(infector, store, initalDT)
                    print(infectees["infecteds"])

    def getTracedContact(self):
        return self.__ordInfPerson

        # if (currentDepth < self.__maxDepth):
        #     stores = ct.getInfStores(55, dt)

        #     print(currentDepth)
        #     currentDepth += 1
        #     self.trace(infector, initalDT, currentDepth)


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
# fillCCustHlthRec(intances=300, people=50)
# instances directly
# people inversely
# timedef inversely


id = 1
ct = Contact(id, db)
dt = ct.setDateEntered()
print(dt)
# stores = ct.getInfStores(55, dt)
# print(stores)
# persons = ct.getInfectees(55, 15, dt)
# print(persons[0])
# stores = ct.getInfStores(45, persons[1])
# print(stores)
ct.trace(id, dt)
print(ct.getTracedContact())
