from database import Database


class ContactTracing():
    def __init__(self, p_infected, p_database, p_maxLevel=3):
        self.__infected = p_infected
        self.__database = p_database
        self.recordedStores = []  # no heirchy
        self.recordedContacts = [self.__infected]  # no heirchy
        self.contact = {}
        self.contact[self.__infected] = None
        self.test(self.contact, self.recordedStores,
                  self.recordedContacts, p_maxLevel)

    def convertToArray(self, arrayOfTup):
        ''' Converts the tuples of IDs to array '''
        ids = []
        for tup in arrayOfTup:
            ids.append(str(tup)[1:-2])
        return ids

    def getInfectedStores(self, infectedPerson, prevRecStores):
        ''' Acceprts array of infected Persons, returns array of infected Stores.
            elemnts from the result that also exist in prevRecStores will be removed '''
        infectedStores = []
        currentInfStore = []

        # query to get the store id visited by the infected user
        currentInfStore = self.convertToArray(db.query(
            "SELECT s_id FROM customers_health_record WHERE u_id = {}".format(infectedPerson)))

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

    def getInfectedPerson(self, infectedStores, prevRecPersons):
        ''' Acceprts array of infected Stores, returns array of infected Users.
            elemnts from the result that also exist in prevRecPerson will be removed '''
        infectedPersons = []
        currentInfStore = []

        for infectedStore in infectedStores:
            infectedStore = str(infectedStore)
            # query to get the user id that went to the specified store id
            currentInfStore = self.convertToArray(db.query(
                "SELECT u_id FROM customers_health_record WHERE s_id = {}".format(infectedStore)))

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

    def test(self, dictStuff, recStores, recPers, maxLevel, level=0):
        if level < maxLevel:
            for key in dictStuff.keys():
                retreivedStores = self.getInfectedStores(key, recStores)
                if len(retreivedStores) != 0:
                    retreivedUsers = self.getInfectedPerson(
                        retreivedStores, recPers)
                    recStores += retreivedStores
                    recPers += retreivedUsers

                    level += 1
                    if (len(retreivedUsers) != 0):
                        dictStuff[key] = dict.fromkeys(retreivedUsers)
                        self.test(dictStuff[key], recStores,
                                  recPers, maxLevel, level)
                    else:
                        dictStuff[key] = None


# db = Database("localhost", "root", "root", "testDB")
# trace = ContactTracing('10', db, 3)
# print(trace.contact)

