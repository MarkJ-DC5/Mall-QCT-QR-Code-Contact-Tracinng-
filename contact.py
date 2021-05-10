from os import O_APPEND
from database_HighControls import HighControlDB
from database import Database, random
from datetime import datetime, timedelta


class Contact():
    def __init__(self, database, depth=3):
        self.__db = database
        self.__primaryInfecteds = []
        self.__Traces = []

    def startTracing(self):
        self.updateTracedDB()
        self.__primaryInfecteds = self.getPrimaryInfecteds()
        self.__Traces = self.multipleTrace(self.__primaryInfecteds)
        self.uploadPrimeInfs()

    def updateTracedDB(self):
        self.__db.query("SET @uids := null")
        self.__db.query("UPDATE primary_infecteds\
                        SET dt_rem = '{}'\
                        WHERE DATEDIFF('{}', DATE(dt_rec)) >= 7 AND dt_rem IS NULL\
                        AND ( SELECT @uids := CONCAT_WS(',', inf_id, @uids))".format(str(datetime.now().replace(microsecond=0)), str(datetime.now().date())))
        self.__db.commit()
        updated = self.__db.query("SELECT @uids;")

        for id in updated:
            if (id != None):
                prevInfecteds = self.singleTrace(id)
                prevInfecteds = tuple(prevInfecteds["histInfecteds"])
                self.__db.query(
                    "UPDATE users SET inf_cov = 'Healthy' WHERE u_id in {}".format(prevInfecteds))
        self.__db.commit()

    def getPrimaryInfecteds(self):
        # from the already recorded
        primaryInfectees = self.__db.query(
            "SELECT inf_id FROM primary_infecteds WHERE dt_rem IS NULL ORDER BY dt_rec desc")

        infecteesCount = len(primaryInfectees)

        if(infecteesCount > 0):
            if(infecteesCount == 1):
                primaryInfectees.append(-1)
            fromUsers = (self.__db.query(
                "SELECT u_id FROM users WHERE inf_cov = 'Primary Inf' AND dt_rem IS NULL and u_id NOT IN {}".format(tuple(primaryInfectees))))

        else:
            fromUsers = (self.__db.query(
                "SELECT u_id FROM users WHERE inf_cov = 'Primary Inf' AND dt_rem IS NULL "))

        primaryInfectees += fromUsers

        self.__primaryInfecteds += primaryInfectees
        return primaryInfectees

    def uploadPrimeInfs(self):
        if(-1 in self.__primaryInfecteds):
            self.__primaryInfecteds.remove(-1)
        for id in self.__primaryInfecteds:
            exist = self.__db.query(
                "SELECT COUNT(*) FROM primary_infecteds WHERE inf_id = {} AND dt_rem IS NULL".format(id))
            exist = exist[0]
            if (exist == 0):
                self.__db.insert("primary_infecteds", ["inf_id", "dt_rec"], [
                                 id, str(datetime.now())])

    def getDTEntered(self, uID):
        dtEntered = self.__db.query(
            "SELECT dt_rec FROM customers_health_record  WHERE u_id = {}  ORDER BY dt_rec DESC LIMIT 1".format(uID))
        if(len(dtEntered) != 0):
            return dtEntered[0]
        else:
            return False

    def __cleanOutputList(self, srcList, refList):
        cleaned = []
        srcLen = len(srcList)

        # removes repeated ID
        cleaned = list(dict.fromkeys(srcList))

        # removes already recorded ID
        if (len(cleaned) > 0):
            currentInd = 0
            cleanedLen = len(cleaned)
            while currentInd < cleanedLen:
                if(cleaned[currentInd] in refList):
                    del cleaned[currentInd]
                    cleanedLen -= 1
                else:
                    currentInd += 1

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

                # get the list of infected person
                tempInfPersons = self.__db.query(
                    "SELECT u_id FROM customers_health_record WHERE s_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infStore, str(dt), str(self.__addOneHr(dt))))

                # removes any form of repition from the result
                tempInfPersons = self.__cleanOutputList(
                    tempInfPersons, histInfPers)

                infPersons.extend(tempInfPersons)
            dtEnt = dtEnt[0]

        # updte history of recorded
        histInfPers += infPersons

        # returns the list of infected people and time the infectore entered the shop
        return {"infecteds": infPersons, "dtEnt": dtEnt}

    def __trace(self, ordInfPerson, initalDT, histInfPers, histInfStores, orderedHistInf, currentDepth=0, maxDepth=3):
        # set the limit for the depth of recursing
        if (currentDepth <= maxDepth):
            # perform tracing for every key in the dictionary of contacts
            for infector in ordInfPerson:

                # update Health Status
                healthStatus = ""
                if (currentDepth == 0):
                    healthStatus = "Primary Inf"
                elif (currentDepth > 0):
                    if (currentDepth == 1):
                        healthStatus = "First Contact"
                    elif (currentDepth == 2):
                        healthStatus = "Second Contact"
                    elif (currentDepth == 3):
                        healthStatus = "Third Contact"
                    orderedHistInf[currentDepth - 1].append(infector)
                self.__db.query("UPDATE users SET inf_cov = '{}' WHERE u_id = {}".format(
                    healthStatus, infector))

                if (currentDepth <= maxDepth and initalDT != None):
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

                    # the dictionary for the contacted people is then set as the value for of the infector key
                    if (len(infectorContacts) > 0):
                        ordInfPerson[infector] = infectorContacts
                        nextDepth = currentDepth + 1
                        self.__trace(infectorContacts,
                                     infectees["dtEnt"], histInfPers, histInfStores, orderedHistInf, nextDepth)

                    elif (len(infectorContacts) == 0):
                        ordInfPerson[infector] = None
            self.__db.commit()
        else:
            return ordInfPerson

    def singleTrace(self, primaryInf):
        traced = {}
        traced[primaryInf] = None
        dtEnt = self.getDTEntered(primaryInf)
        histInfecteds = [primaryInf]
        hsitInfectedStores = []
        orderedHistInf = [[], [], []]
        self.__trace(traced, dtEnt, histInfecteds,
                     hsitInfectedStores, orderedHistInf)
        return {"traced": traced, "orderedHistInf": orderedHistInf, "histInfecteds": histInfecteds, "hsitInfectedStores": hsitInfectedStores}

    def multipleTrace(self, primaryInfectees):
        byContactTrace = []
        byDepthTrace = {}
        for primeInf in primaryInfectees:
            dtEnt = self.getDTEntered(primeInf)
            if(dtEnt != False):
                trace = self.singleTrace(primeInf)
                byContactTrace.append(trace["traced"])
                byDepthTrace[primeInf] = trace["orderedHistInf"]

        return {"byContactTrace": byContactTrace, "byDepthTrace": byDepthTrace}

    def getTracedContact(self):
        return self.__Traces


def resetCustHlthRec():
    db = HighControlDB()
    db.query("DROP TABLE IF EXISTS Customers_Health_Record")
    db.query("CREATE TABLE Customers_Health_Record (\
        u_id int,\
        s_id int,\
        dt_rec datetime NOT NULL)")
    print("Customers_Health_Record Table Created")


def fillCCustHlthRec(intances=100, people=100, stores=15, timeDif=24):
    db = HighControlDB()
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


def TestTrace():
    db = HighControlDB()
    # uncomment if customer_health_records need to be resetted and filled
    # resetCustHlthRec()
    # fillCCustHlthRec(intances=2500, people=100, timeDif=72)
    # instances directly proportional to trace contact outputs
    # people inversely proportional
    # timedef inversely proportional

    # test every possible primaryInfectedId
    ct = Contact(db)
    traced = ct.singleTrace(64)
    print(traced)
    # i = 1
    # while i <= 100:
    #     id = i
    #     ct = Contact(db)
    #     traced = ct.singleTrace(id)
    #     traced = traced["traced"]
    #     print(traced)
    #     i += 1
