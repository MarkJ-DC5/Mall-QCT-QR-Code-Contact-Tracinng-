from database_HighControls import HighControlDB, random
from datetime import datetime, timedelta

# To do
# Handle multiple traces
# Save uID of first infected in database
# Delete trace after 7days


class ContactTracing():
    def __init__(self, p_infected, p_database, p_dtStr, p_maxLevel=3):
        self.__infected = p_infected
        self.__database = p_database
        self.__dateInfected = p_dtStr
        self.recordedStores = []  # no heirchy
        self.recordedContacts = [self.__infected]  # no heirchy
        self.contact = {}
        self.contact[self.__infected] = None
        self.TraceContacts(self.contact, self.recordedStores,
                           self.recordedContacts, p_dtStr, p_maxLevel)

    def convertToArray(self, arrayOfTup):
        ''' Converts the tuples of IDs to array '''
        ids = []
        if (type(arrayOfTup) == tuple):
            for tup in arrayOfTup:
                ids.append(str(tup))
        else:
            for tup in arrayOfTup:
                ids.append(str(tup[0]))
        return ids

    def incrementHR(self, dtStr):
        dtObj = datetime.strptime(
            dtStr, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
        return str(dtObj)

    def getInfectedStores(self, infectedPerson, prevRecStores, dtStr):
        ''' Acceprts array of infected Persons, returns array of infected Stores.
            elemnts from the result that also exist in prevRecStores will be removed '''
        infectedStores = []
        currentInfStore = []

        # query to get the store id visited by the infected user
        currentInfStore = self.convertToArray(db.query(
            "SELECT s_id FROM customers_health_record WHERE u_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infectedPerson, dtStr, self.incrementHR(dtStr))))

        # remove repeatition
        infectedStores += list(dict.fromkeys(currentInfStore))

        # remove repeatition
        infectedStores = list(dict.fromkeys(infectedStores))

        # remove already recorded store
        if(len(infectedStores) > 0):
            for prev in prevRecStores:
                try:
                    del infectedStores[infectedStores.index(
                        prev)]
                except:
                    pass

        return infectedStores

    def getInfectedPerson(self, infectedStores, prevRecPersons, dtStr):
        ''' Acceprts array of infected Stores, returns array of infected Users.
            elemnts from the result that also exist in prevRecPerson will be removed '''
        infectedPersons = []
        currentInfStore = []

        for infectedStore in infectedStores:
            infectedStore = str(infectedStore)
            # query to get the user id that went to the specified store id
            currentInfStore = self.convertToArray(db.query(
                "SELECT u_id FROM customers_health_record WHERE s_id = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(infectedStore, dtStr, self.incrementHR(dtStr))))

            # remove repeatition
            infectedPersons += list(dict.fromkeys(currentInfStore))

        # remove repeatition
        infectedPersons = list(dict.fromkeys(infectedPersons))

        # remove already recorded user
        if(len(infectedPersons) > 0):
            for prev in prevRecPersons:
                try:
                    del infectedPersons[infectedPersons.index(
                        prev)]
                except:
                    pass

        return infectedPersons

    def TraceContacts(self, traced, recStores, recPers, dtStr, maxLevel, level=0):
        if level < maxLevel:
            for key in traced.keys():
                retreivedStores = self.getInfectedStores(key, recStores, dtStr)
                if len(retreivedStores) != 0:
                    retreivedUsers = self.getInfectedPerson(
                        retreivedStores, recPers, dtStr)
                    recStores += retreivedStores
                    recPers += retreivedUsers

                    level += 1
                    # if (len(retreivedUsers) != 0):
                    #     traced[key] = dict.fromkeys(retreivedUsers)
                    #     self.TraceContacts(traced[key], recStores,
                    #                        recPers, self.incrementHR(dtStr), maxLevel, level)
                    # else:
                    #     traced[key] = None


db = HighControlDB("f", fileName="develop/dbTestCred.txt")


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
# fillCCustHlthRec(intances=500, timeDif=0)


# update; first stores should be filtered by day only
trace = ContactTracing('55', db, "2021-05-06 14:56:53", 3)
print(trace.contact)
