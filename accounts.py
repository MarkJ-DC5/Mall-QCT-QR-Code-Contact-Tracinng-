from datetime import date
from typing import ItemsView
from user import *


class Customer(User):
    def readQR(self, img):
        try:
            val, points, straight_qrcode = cv.QRCodeDetector().detectAndDecode(cv.imread(img))
            try:
                data = self._db.query(
                    "SELECT * FROM stores WHERE s_ID IN (\"{}\")".format(val))
                if (data != False):
                    if (data != []):
                        print(data)
                        self._db.insert("customers_health_record",
                                        ["u_id", "s_id", "dt_rec"], [self._info["uID"], data[0], str(
                                            datetime.now().replace(microsecond=0))])
                        return True
                    else:
                        print("No Matching Store")

            except Exception as e:
                print(e)
                print("Error Retriving Data")
        except:
            print("Error in Reading QR Code")
        return False

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
        tempData = self._db.query(
            "SELECT store_num, floor, wing, name FROM stores WHERE store_num = {}".format(storeNum))
        data = {}
        if (tempData != False):
            if (len(tempData) > 0):
                data["sNum"] = tempData[0]
                data["floor"] = tempData[1]
                data["wing"] = tempData[2]
                data["name"] = tempData[3]
                return data
        else:
            return None

    def getHistory(self, instances=5):
        history = []
        # {"date": None, "store": []}

        tempDates = self._db.query(
            "SELECT DISTINCT DATE(dt_rec) FROM customers_health_record WHERE u_id = {} LIMIT {}".format(self._info['uID'], instances))
        if (tempDates != None):
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
        # SELECT DISTINCT DATE(dt_rec) FROM customers_health_record WHERE u_id = 1 LIMIT 5
        # SELECT DISTINCT s_id FROM customers_health_record WHERE DATE(dt_rec) = "2021-05-05" AND u_id = 1


class Admin(User):
    def __init__(self, database, qrCodePath="QRcodes/"):
        # prevent overiding of parent's init
        User.__init__(self, database)
        super().__init__(database)  # inherits all methods and properties
        self.__qrCodePath = qrCodePath

    def getStoreInfo(self, storeNum):
        tempData = self._db.query(
            "SELECT * FROM stores WHERE store_num = {}".format(storeNum))
        data = {}
        if (tempData != False):
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
            return None

    def generateQRCode(self, storeInfo):
        if (storeInfo[0] != None):
            id_qrCode = qrcode.make(storeInfo[0])
            qrName = str(storeInfo[0]) + "_" + \
                str(storeInfo[1]) + "_" + storeInfo[4] + ".jpg"
            id_qrCode.save(self.__qrCodePath + qrName)
            print(qrName, "generated")
        else:
            print("No data passed")
