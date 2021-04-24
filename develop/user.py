from database import *


class User:
    _db = Database("localhost", "root", "root", "Development")

    def __init__(self):
        self.info = {'uID': None,
                     'cNum': None,
                     'passwd': None,
                     'infCov': None,
                     'fName': None,
                     'mName': None,
                     'lName': None,
                     'age': None,
                     'gender': None,
                     'street': None,
                     'barangay': None,
                     'city': None,
                     'country': None,
                     'dtAdd': None,
                     'dtRem': None, }

    def newUser(self, p_cNum, p_passwd, p_infCov,
                p_fName, p_mName, p_lName, p_age, p_gender,
                p_street, p_barangay, p_city, p_country):
        # """ Inserts the passed info of new user to the database """"
        values = [p_cNum, p_passwd, p_infCov,
                  p_fName, p_mName, p_lName, p_age, p_gender,
                  p_street, p_barangay, p_city, p_country, str(datetime.now().date())]

        self._db.insert("Users", ["c_num", "passwd", "inf_cov", "f_name", "m_name", "l_name", "age",
                                  "gender", "street", "barangay", "city", "country", "dt_add"], values)

    def loadData(self, data):
        # """ Loads data passed by the verify userFunction """"
        i = 0
        for col in self.info:
            self.info[col] = data[0][i]
            i += 1

    def verifyUser(self, p_cNum, p_passwd):
        # """ Returns true if user is in database and loads info locally.
        #     Returns false otherwise """"
        data = self._db.query(
            "SELECT * FROM Users WHERE c_num IN (\"{}\") AND passwd IN (\"{}\") ".format(p_cNum, p_passwd))

        if(data != []):
            self.loadData(data)
            return True
        else:
            return False

    def getTotalCount(self, datetime):
        # """ Returns the total count of customer upto the given time """
        pass

    def getShopsWithLowCount(self, datetime):
        # """ Returns 5 shops with the lowest count """
        pass

    def getShopsWithHighCount(self, datetime):
        # """ Returns 5 shops with the hgihest count """
        pass
