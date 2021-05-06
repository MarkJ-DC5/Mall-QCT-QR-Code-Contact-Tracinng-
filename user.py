from logging import raiseExceptions
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

    def newUser(self, p_cNum, p_passwd, p_type,
                p_fName, p_lName, p_age, p_gender,
                p_street, p_barangay, p_city):
        values = [p_cNum, p_passwd,  p_type, "Healthy",
                  p_fName, p_lName, p_age, p_gender,
                  p_street, p_barangay, p_city, str(datetime.now().date())]

        numOfExisting = self._db.query(
            "SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(p_cNum))
        numOfExisting = numOfExisting[0]

        if (numOfExisting == 0):
            self._db.insert("Users", ["c_num", "passwd", "type", "inf_cov", "f_name", "l_name", "age",
                                      "gender", "street", "barangay", "city", "dt_add"], values)
            return True
        elif(numOfExisting > 0):
            print('Contact Number Already Exist')
            return False

    def removeUser(self):
        if(self._info["uID"] != None):
            data = self._db.query(
                "SELECT * FROM users WHERE u_id = {}".format(self._info["uID"]))
            if (len(data) > 0):
                if(data[-1] == None):
                    self._db.update("users", ["dt_rem"], [str(
                        datetime.now().date())], "u_id = {}".format(self._info["uID"]))
                    return True
                else:
                    print("Already Deleted")
            else:
                print("{} u_id Not Found".format(self._info["uID"]))
        else:
            print("u_id from argument is Invalid")
        return False

    def __loadData(self, data):
        i = 0
        for col in self._info:
            self._info[col] = data[i]
            i += 1

    def verifyUser(self, p_cNum, p_passwd):
        data = self._db.query(
            "SELECT * FROM Users WHERE c_num IN (\"{}\") AND passwd IN (\"{}\") ".format(p_cNum, p_passwd))

        if(data != None and len(data) > 0 and data[-1] == None):
            self.__loadData(data)
            self._isVerified = True
            return True
        else:
            return False

    def getUserType(self):
        return self._info['type']

    def setInfo(self, info):
        self._info = info

    def transferInfoTo(self, child):
        child.setInfo(self._info)

    def countEntered(self):
        counted = self._db.query("SELECT COUNT(DISTINCT u_id) FROM customers_health_record WHERE dt_rec LIKE \"{}%\"".format(
            str(datetime.now().date())))
        counted = counted[0]
        return counted

    def getStoreInfo(self, storeNum):
        data = self._db.query(
            "SELECT s_id FROM stores WHERE store_num = {}".format(storeNum))
        if (len(data) > 0):
            return data
        else:
            print("{} store num Not Found".format(storeNum))
            return False

    def getStoreWithHighCount(self):
        stores = []
        tempStores = self._db.query("SELECT s_id, COUNT(*) AS occurrences FROM customers_health_record WHERE dt_rec BETWEEN \"{0} 0:00:00\" AND \"{0} 23:59:00\" GROUP BY s_id ORDER BY occurrences DESC LIMIT 5".format(
            str(datetime.now().date())))

        for store in tempStores:
            info = self.getStoreInfo(store[0])
            if (info != None):
                stores.append({"count": store[1], "store": info})
        return stores

    def getStoreWithLowCount(self):
        stores = []
        tempStores = self._db.query("SELECT s_id, COUNT(*) AS occurrences FROM customers_health_record WHERE dt_rec BETWEEN \"{0} 0:00:00\" AND \"{0} 23:59:00\" GROUP BY s_id ORDER BY occurrences ASC LIMIT 5".format(
            str(datetime.now().date())))

        for store in tempStores:
            info = self.getStoreInfo(store[0])
            if (info != None):
                stores.append({"count": store[1], "store": info})
        return stores

    def updateInfo(self, cols, values):
        forbidden = ("u_id", "type", "inf_cov", "dt_add", "dt_rem")

        colCount = len(cols)
        i = 0
        while (i < colCount):
            if cols[i] in forbidden:
                del cols[i]
                del values[i]
                colCount -= 1
            else:
                i += 1

        numOfExisting = self._db.query(
            "SELECT COUNT(c_num) FROM users WHERE c_num IN (\"{}\")".format(values[cols.index("c_num")]))
        numOfExisting = numOfExisting[0]

        if (numOfExisting == 0):
            self._db.update("users", cols, values,
                            "u_id = {}".format(self._info["uID"]))
        elif(numOfExisting > 0):
            print('Contact Number Already Exist')
            return False

    def deleteAccount(self):
        currentDTRem = self._db.query(
            "SELECT dt_rem FROM users WHERE u_id = {}".format(self._info['uID']))

        if (currentDTRem != None):
            self._db.update('users', ["dt_rem"], [
                str(datetime.now().date())], "u_id = {}".format(self._info['uID']))
        else:
            print("Already Deleted on {}".format(currentDTRem))

    def __del__(self):
        print("Deleting Instance")
