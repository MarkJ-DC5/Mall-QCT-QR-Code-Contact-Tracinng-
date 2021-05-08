from random import randrange
from typing import Counter
import cv2 as cv
import qrcode
from PIL import Image

from database import Database, datetime


class User:
    def __init__(self, database):
        self._db = database
        self._isVerified = False
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
                      'dtAdd': None,
                      'dtRem': None, }

    def __loadData(self, data):
        i = 0
        for col in self._info:
            self._info[col] = data[i]
            i += 1

    def verifyUser(self, p_cNum, p_passwd):
        data = self._db.query(
            "SELECT * FROM Users WHERE c_num = {} AND passwd = \"{}\" ".format(p_cNum, p_passwd))

        if(data != None and len(data) > 0 and data[-1] == None):
            self.__loadData(data)
            self._isVerified = True
            return True
        else:
            return False

    def newUser(self, p_cNum, p_passwd, p_type,
                p_fName, p_lName, p_age, p_gender,
                p_street, p_barangay, p_city):

        values = [p_cNum, p_passwd,  p_type, "Healthy",
                  p_fName, p_lName, p_age, p_gender,
                  p_street, p_barangay, p_city, str(datetime.now().date())]

        # check existance of same number before insertion
        numOfExisting = self._db.query(
            "SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(p_cNum))

        if (numOfExisting == 0):
            self._db.insert("Users", ["c_num", "passwd", "type", "inf_cov", "f_name", "l_name", "age",
                                      "gender", "street", "barangay", "city", "dt_add"], values)
            return True

        elif(numOfExisting > 0):
            print('Contact Number Already Exist')
            return False

    def getUserType(self):
        return self._info['type']

    def updateInfo(self, cols, values):
        forbidden = ("u_id", "type", "inf_cov", "dt_add", "dt_rem")
        if (self._isVerified):
            colLen = len(cols)
            i = 0
            while (i < colLen):
                if cols[i] in forbidden:
                    del cols[i]
                    del values[i]
                    colLen -= 1
                else:
                    i += 1

            numOfExisting = self._db.query(
                "SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(values[cols.index("c_num")]))

            if (numOfExisting == 0):
                self._db.update("users", cols, values,
                                "u_id = {}".format(self._info["uID"]))
                return True
            elif(numOfExisting > 0):
                print('Contact Number Already Exist')
                return False
        else:
            return False

    def deleteAccount(self):
        if (self._isVerified):
            currentDTRem = self._db.query(
                "SELECT dt_rem FROM users WHERE u_id = {}".format(self._info['uID']))

            if (currentDTRem == None):
                self._db.update('users', ["dt_rem"], [
                    str(datetime.now().date())], "u_id = {}".format(self._info['uID']))
            else:
                print("Already Deleted on {}".format(currentDTRem))
        else:
            return False

    def setInfo(self, info):
        # used by transferInfoTO
        self._info = info

    def transferInfoTo(self, child):
        # transfer info from User to Admin or Customer
        if (self._isVerified):
            child.setInfo(self._info)
        else:
            return False

    def countEntered(self):
        counted = self._db.query("SELECT COUNT(DISTINCT u_id) FROM customers_health_record WHERE dt_rec LIKE \"{}%\"".format(
            str(datetime.now().date())))
        return counted

    def getStoreInfo(self, storeNum):
        # overidden by Customer and Admin
        storeInfo = self._db.query(
            "SELECT s_id FROM stores WHERE store_num = {}".format(storeNum))
        if (type(storeInfo) == int):
            return storeInfo
        else:
            print("{} store num Not Found".format(storeNum))
            return False

    def getStoreWithHighCount(self):
        stores = []
        tempStores = self._db.query("SELECT s_id, COUNT(*) AS occurrences FROM customers_health_record WHERE dt_rec LIKE '{}%' GROUP BY s_id ORDER BY occurrences DESC LIMIT 5".format(
            str(datetime.now().date())))

        for store in tempStores:
            # store is formatted as (s_id, count)
            storeInfo = self.getStoreInfo(store[0])
            if (storeInfo != None):
                stores.append({"store": storeInfo, "count": store[1]})
        return stores

    def getStoreWithLowCount(self):
        stores = []
        tempStores = self._db.query("SELECT s_id, COUNT(*) AS occurrences FROM customers_health_record WHERE dt_rec LIKE '{}%' GROUP BY s_id ORDER BY occurrences ASC LIMIT 5".format(
            str(datetime.now().date())))

        for store in tempStores:
            # store is formatted as (s_id, count)
            storeInfo = self.getStoreInfo(store[0])
            if (storeInfo != None):
                stores.append({"store": storeInfo, "count": store[1]})
        return stores

    def __del__(self):
        print("Deleting Instance")
