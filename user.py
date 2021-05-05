import cv2 as cv
import qrcode
from PIL import Image

from database import Database, datetime


class User:
    def __init__(self, database):
        self._db = database
        self._info = {'uID': None,
                      'cNum': None,
                      'passwd': None,
                      'type': None,
                      'infCov': None,
                      'fName': None,
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
                p_fName, p_lName, p_age, p_gender,
                p_street, p_barangay, p_city, p_country):
        # """ Inserts the passed info of new user to the database """"
        values = [p_cNum, p_passwd,  p_type, p_infCov,
                  p_fName, p_lName, p_age, p_gender,
                  p_street, p_barangay, p_city, p_country, str(datetime.now().date())]
        numOfExisting = self._db.query(
            "SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(p_cNum))
        numOfExisting = numOfExisting[0]
        print(numOfExisting)
        if (numOfExisting == 0):
            self._db.insert("Users", ["c_num", "passwd", "type", "inf_cov", "f_name", "l_name", "age",
                                      "gender", "street", "barangay", "city", "country", "dt_add"], values)
        elif(numOfExisting > 0):
            print('Already Exist')

    def removeUser(self):
        if(self._info["uID"] != None):
            data = self._db.query(
                "SELECT * FROM users WHERE u_id = {}".format(self._info["uID"]))
            if (data != False):
                self._db.update("users", ["dt_rem"], [str(
                    datetime.now().date())], "u_id = {}".format(self._info["uID"]))

    def __loadData(self, data):
        # """ Loads data passed by the verify userFunction """"
        i = 0
        for col in self._info:
            self._info[col] = data[i]
            i += 1

    def verifyUser(self, p_cNum, p_passwd):
        # """ Returns true if user is in database and loads info locally.
        #     Returns false otherwise """"
        data = self._db.query(
            "SELECT * FROM Users WHERE c_num IN (\"{}\") AND passwd IN (\"{}\") ".format(p_cNum, p_passwd))

        if(data != False and data != [] and data[-1] == None):
            self.__loadData(data)
            return True
        else:
            return False

    def getType(self):
        return self._info['type']

    def setInfo(self, info):
        self._info = info

    def transferInfoTo(self, child):
        child.setInfo(self._info)

    def __del__(self):
        print("Deleting Instance")
