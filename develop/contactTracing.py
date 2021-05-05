from database import Database
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
        for tup in arrayOfTup:
            ids.append(str(tup)[1:-2])
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
                    if (len(retreivedUsers) != 0):
                        traced[key] = dict.fromkeys(retreivedUsers)
                        self.TraceContacts(traced[key], recStores,
                                           recPers, self.incrementHR(dtStr), maxLevel, level)
                    else:
                        traced[key] = None


db = Database("f", self._fileName="develop/dbTestCred.txt")
# update; first stores should be filtered by day only
trace = ContactTracing('46', db, "2021-04-25 17:39:30", 3)
print(trace.contact)
