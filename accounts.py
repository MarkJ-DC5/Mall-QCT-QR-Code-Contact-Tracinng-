from datetime import date, timedelta
from logging import exception
from typing import ItemsView
from user import *


class Customer(User):
    def readQR(self, img):
        try:
            try:
                val, points, straight_qrcode = cv.QRCodeDetector().detectAndDecode(cv.imread(img))
            except:
                raise Exception("Error in Reading QR Code")
            store = self._db.query(
                "SELECT * FROM stores WHERE s_ID IN (\"{}\")".format(val))
            if (store != None):
                if (len(store) > 0):
                    currentDT = datetime.now().replace(microsecond=0)

                    recorded = self._db.query(
                        "SELECT COUNT(*) FROM customers_health_record WHERE u_ID = {} AND s_ID = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(
                            self._info["uID"], store[0], str(currentDT - timedelta(minutes=10)), str(currentDT)))
                    recorded = recorded[0]

                    if (recorded == 0):
                        self._db.insert("customers_health_record",
                                        ["u_id", "s_id", "dt_rec"], [self._info["uID"], store[0], str(currentDT)])
                        return True
                    else:
                        raise Exception("Already Added")
                else:
                    raise Exception("{} s_id Not found".format(val))
            else:
                raise Exception("Error in Query")
        except Exception as e:
            print(e)
            return None

    def getInfo(self):
        info = {'name': None, 'infCov': None,
                'age': None, 'gender': None, 'address': None}
        # infCovType = {'NC': "No Contact", 'PC': "Primary Infected",
        #               'FC': "First Contact", 'SC': "Second Contact", 'TC': "Third Contact"}
        if (self._isVerified):
            info['name'] = self._info['fName'] + " " + self._info['lName']
            info['infCov'] = self._info['infCov']
            info['age'] = self._info['age']
            info['gender'] = self._info['gender']
            info['address'] = self._info['street'] + ", " + \
                self._info['barangay'] + ", " + \
                self._info['street'] + ", " + self._info['city']
            return info

    def getStoreInfo(self, storeNum):
        try:
            tempData = self._db.query(
                "SELECT store_num, floor, wing, name FROM stores WHERE store_num = {}".format(storeNum))
            data = {}
            if (tempData != None):
                if (len(tempData) > 0):
                    data["sNum"] = tempData[0]
                    data["floor"] = tempData[1]
                    data["wing"] = tempData[2]
                    data["name"] = tempData[3]
                    return data
                else:
                    raise Exception("{} store_num Not Found".format(storeNum))
            else:
                raise Exception("Error in Query")
        except Exception as e:
            print(e)
            return None

    def getHistory(self, instances=5):
        try:
            history = []
            tempDates = self._db.query(
                "SELECT DISTINCT DATE(dt_rec) FROM customers_health_record WHERE u_id = {} LIMIT {}".format(self._info['uID'], instances))

            if (tempDates != None):
                if (len(tempDates) > 0):
                    for d in tempDates:
                        log = {"date": None, "stores": []}
                        d = str(d)
                        log['date'] = d

                        tempStores = self._db.query(
                            "SELECT s_id, MAX(TIME(dt_rec)) FROM customers_health_record WHERE DATE(dt_rec) = \"{}\" AND u_id = {} GROUP BY s_id".format(d, self._info['uID']))
                        # print(tempStores)
                        if (tempStores != None):
                            for store in tempStores:
                                storeInfo = self.getStoreInfo(store[0])
                                storeInfo["timeEnt"] = str(store[1])
                                log['stores'].append(storeInfo)
                        history.append(log)
                    print(history)
                else:
                    raise Exception(
                        "{} u_id Not Found".format(self._info['uID']))
            else:
                raise Exception("Error in Query")
        except Exception as e:
            print(e)
            return None


class Admin(User):
    def __init__(self, database, qrCodePath="QRcodes/"):
        # prevent overiding of parent's init
        User.__init__(self, database)
        super().__init__(database)  # inherits all methods and properties
        self.__qrCodePath = qrCodePath

    def getStoreInfo(self, storeNum):
        try:
            tempData = self._db.query(
                "SELECT * FROM stores WHERE store_num = {}".format(storeNum))
            data = {}
            if (tempData != None):
                if (len(tempData) > 0):
                    data["sID"] = tempData[0]
                    data["sNum"] = tempData[1]
                    data["floor"] = tempData[2]
                    data["wing"] = tempData[3]
                    data["name"] = tempData[4]
                    data["cNum"] = tempData[5]
                    data["email"] = tempData[6]
                    data["dt_add"] = tempData[7]
                    data["dt_rem"] = tempData[8]
                    return data
                else:
                    raise Exception("{} store_num Not Found".format(storeNum))
            else:
                raise Exception("Error in Query")
        except Exception as e:
            print(e)
            return None

    def generateQRCode(self, storeInfo):
        try:
            if (storeInfo["sID"] != None):
                id_qrCode = qrcode.make(storeInfo["sID"])
                qrName = str(storeInfo["sID"]) + "_" + \
                    str(storeInfo["sNum"]) + "_" + storeInfo["name"] + ".jpg"
                id_qrCode.save(self.__qrCodePath + qrName)
                print(qrName, "generated")
            else:
                raise Exception("Passed Argmument Not Valid")
        except Exception as e:
            print(e)
            return None
        else:
            print("No data passed")
