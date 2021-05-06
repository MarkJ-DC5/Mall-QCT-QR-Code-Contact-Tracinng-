from datetime import date, timedelta
from logging import exception
from types import CoroutineType
from typing import ItemsView
from user import *
import base64


class Customer(User):
    def readQR(self, img):
        try:
            try:
                val, points, straight_qrcode = cv.QRCodeDetector().detectAndDecode(cv.imread(img))
            except:
                raise Exception("Error in Reading QR Code")
            store = self._db.query(
                "SELECT * FROM stores WHERE s_ID IN (\"{}\")".format(val))
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
                    print("Already Added")
            else:
                print("{} s_id Not found".format(val))
            return False
        except Exception as e:
            print(e)
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
        else:
            return False

    def getStoreInfo(self, storeNum):
        tempData = self._db.query(
            "SELECT store_num, floor, wing, name FROM stores WHERE store_num = {}".format(storeNum))
        data = {}

        if (len(tempData) > 0):
            data["sNum"] = tempData[0]
            data["floor"] = tempData[1]
            data["wing"] = tempData[2]
            data["name"] = tempData[3]
            return data
        else:
            print("{} store_num Not Found".format(storeNum))
            return False

    def getHistory(self, instances=5):
        history = []
        tempDates = self._db.query(
            "SELECT DISTINCT DATE(dt_rec) FROM customers_health_record WHERE u_id = {} LIMIT {}".format(self._info['uID'], instances))

        if (len(tempDates) > 0):
            for d in tempDates:
                log = {"date": None, "stores": []}
                d = str(d)
                log['date'] = d

                tempStores = self._db.query(
                    "SELECT s_id, MAX(TIME(dt_rec)) FROM customers_health_record WHERE DATE(dt_rec) = \"{}\" AND u_id = {} GROUP BY s_id".format(d, self._info['uID']))

                if (tempStores != None):
                    for store in tempStores:
                        storeInfo = self.getStoreInfo(store[0])
                        storeInfo["timeEnt"] = str(store[1])
                        log['stores'].append(storeInfo)
                history.append(log)
            return history
        else:
            print("{} u_id Not Found".format(self._info['uID']))
            return False

    def uploadProof(self, proof):
        currentDT = datetime.now().replace(microsecond=0)
        latestEntryCount = self._db.query("SELECT COUNT(uploaded_by) FROM proof_records WHERE dt_uploaded BETWEEN \"{}\" and \"{}\"".format(
            str(currentDT - timedelta(hours=1)), str(currentDT)))

        if (latestEntryCount == 0):
            self._db.insert("proof_records", ["proofLink", "uploaded_by", "dt_uploaded"], [
                            proof, self._info["uID"], str(datetime.now().replace(microsecond=0))])
            return True
        else:
            print("Already Have an Entry within an Hour Ago")
            return False

    def updateHealthStatus(self):
        proof = self._db.query(
            "SELECT DISTINCT * FROM proof_records WHERE uploaded_by = {}".format(self._info["uID"]))
        if (len(proof) > 0):
            if (proof[4] == 'Approved' and proof[5] != None and proof[6] != None):
                self._info["infCov"] = "Primary Inf"
                self._db.update("users", ["inf_cov"], [
                                self._info["infCov"]], "u_id = {}".format(self._info["uID"]))
            # if (proof[4] == 'Pending'):

        else:
            print("{} uploaded_by Not Found".format(self._info["uID"]))


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
            print("{} store_num Not Found".format(storeNum))
            return False

    def generateQRCode(self, storeInfo):
        try:
            id_qrCode = qrcode.make(storeInfo["sID"])
            qrName = str(storeInfo["sID"]) + "_" + \
                str(storeInfo["sNum"]) + "_" + storeInfo["name"] + ".jpg"
            id_qrCode.save(self.__qrCodePath + qrName)
            return True
        except Exception as e:
            print(e)
            return False

    def getPendingProof(self, intances=5):
        pending = []
        tempPending = self._db.query(
            "SELECT * FROM proof_records WHERE status = 'Pending' ORDER BY dt_uploaded DESC")

        if (len(tempPending) != 0):
            if(type(tempPending) == list and type(tempPending[0]) == tuple):
                for t in tempPending:
                    que = {}
                    que["pID"] = t[0]
                    que["proofLink"] = t[1]
                    que["uploadedBy"] = t[2]
                    que["dtUploaded"] = str(t[3])
                    que["status"] = t[4]
                    que["statChangedBy"] = t[5]
                    que["dtStatChanged"] = t[6]
                    pending.append(que)
            else:
                que = {}
                que["pID"] = tempPending[0]
                que["proofLink"] = tempPending[1]
                que["uploadedBy"] = tempPending[2]
                que["dtUploaded"] = str(tempPending[3])
                que["status"] = tempPending[4]
                que["statChangedBy"] = tempPending[5]
                que["dtStatChanged"] = tempPending[6]
                pending.append(que)

        return pending

    def updateProofStat(self, pID, status):
        if (status == 'Approved' or status == 'Denied' or status == 'Pending'):
            self._db.update("proof_records", ["status", "stat_changed_by", "dt_stat_changed"], [
                            status, self._info["uID"], str(datetime.now().replace(microsecond=0))], "p_id = {}".format(pID))
            return True
        else:
            return False

    def deleteStore(self, id):
        currentDTRem = self._db.query(
            "SELECT dt_rem FROM stores WHERE s_id = {}".format(id))

        if (currentDTRem != None):
            self._db.update('stores', ["dt_rem"], [
                str(datetime.now().date())], "s_id = {}".format(id))
        else:
            print("Already Deleted on {}".format(currentDTRem))

    def newStore(self, p_storeNum, p_floor, p_wing, p_name, p_cNum, p_email):
        existingStore = self._db.query(
            "SELECT COUNT(store_num) FROM stores WHERE store_num = {} AND dt_rem IS NULL".format(p_storeNum))
        existingStore = existingStore[0]
        if (existingStore == 0):
            self._db.insert("stores", ["store_num", "floor", "wing", "name", "c_num", "email", "dt_add"], [
                            p_storeNum, p_floor, p_wing, p_name, p_cNum, p_email, str(datetime.now().date())])
        else:
            print("{} store_num Already Exist".format(p_storeNum))
        # def updateStoreInfo(self, sID, cols, values):
        #     try:
        #         toRemove = cols.index("s_id")
        #         del cols[toRemove]
        #         del values[toRemove]
        #     except ValueError:
        #         pass

        #     numOfExisting = self._db.query(
        #         "SELECT COUNT(c_num) FROM stores WHERE store_num = {} AND dt_rem != None".format(values[cols.index("c_num")]))
        #     numOfExisting = numOfExisting[0]

        #     if (numOfExisting == 0):
        #         self._db.update("stores", cols, values,
        #                         "s_id = {}".format(sID))
        #     elif(numOfExisting > 0):
        #         print('Store Number Already Exist')
        #         return False

    def getStores(self):
        tempStores = self._db.query(
            "Select * FROM stores WHERE dt_rem IS NULL")
        stores = []
        for tStore in tempStores:
            store = {}
            store["sID"] = tStore[0]
            store["store_num"] = tStore[1]
            store["floor"] = tStore[2]
            store["wing"] = tStore[3]
            store["name"] = tStore[4]
            store["cNum"] = tStore[5]
            store["email"] = tStore[6]
            store["dtAdd"] = tStore[7]
            store["dtRem"] = tStore[8]
            stores.append(store)
        return stores
