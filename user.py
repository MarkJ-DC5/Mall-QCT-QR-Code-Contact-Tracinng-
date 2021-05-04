from database import *


class User:
    def __init__(self, database):
        self.__db = database
        self.__info = {'uID': None,
                       'cNum': None,
                       'passwd': None,
                       'type': None,
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

    def newUser(self, p_cNum, p_passwd, p_type, p_infCov,
                p_fName, p_mName, p_lName, p_age, p_gender,
                p_street, p_barangay, p_city, p_country):
        # """ Inserts the passed info of new user to the database """"
        values = [p_cNum, p_passwd,  p_type, p_infCov,
                  p_fName, p_mName, p_lName, p_age, p_gender,
                  p_street, p_barangay, p_city, p_country, str(datetime.now().date())]

        if (self.__db.query("SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(p_cNum)) == 0):
            self.__db.insert("Users", ["c_num", "passwd", "type", "inf_cov", "f_name", "m_name", "l_name", "age",
                                       "gender", "street", "barangay", "city", "country", "dt_add"], values)
        else:
            print('Already Exist')

    def removeUser(self):
        if(self.__info["uID"] != None):
            print(self.__db.query(
                "SELECT * FROM users WHERE u_id = {}".format(self.__info["uID"])))
            self.__db.update("users", ["dt_rem"], [str(
                datetime.now().date())], "u_id = {}".format(self.__info["uID"]))

    def __loadData(self, data):
        # """ Loads data passed by the verify userFunction """"
        i = 0
        for col in self.__info:
            self.__info[col] = data[0][i]
            i += 1

    def verifyUser(self, p_cNum, p_passwd):
        # """ Returns true if user is in database and loads info locally.
        #     Returns false otherwise """"
        data = self.__db.query(
            "SELECT * FROM Users WHERE c_num IN (\"{}\") AND passwd IN (\"{}\") ".format(p_cNum, p_passwd))

        if(data != [] and data[0][-1] == None):
            self.__loadData(data)
            return True
        else:
            return False

    def getType(self):
        return self.__info['type']

    def setInfo(self, info):
        self.__info = info

    def transferInfoTo(self, child):
        child.setInfo(self.__info)

    def __del__(self):
        print("Deleting Instance")
