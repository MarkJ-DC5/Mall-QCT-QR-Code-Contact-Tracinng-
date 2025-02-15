from os import system
from contact import Contact
from datetime import date, timedelta
from logging import exception
from types import CoroutineType
from typing import ItemsView
from user import *
import base64
from pyzbar.pyzbar import decode
import time


class Customer(User):
    def scanQRCode(self):
        try:
            if (self._isVerified):
                cap = cv.VideoCapture(0, cv.CAP_DSHOW)
                cap.set(3, 640)
                cap.set(5, 480)
                content = None
                scanning = True

                try:
                    while scanning == True:
                        success, frame = cap.read()

                        cv.imshow("Scanning...", frame)
                        cv.waitKey(1)

                        for code in decode(frame):
                            content = code.data.decode('utf-8')
                            scanning = False
                            cv.destroyAllWindows()
                            time.sleep(.1)

                except KeyboardInterrupt:
                    print("Press Ctrl-C to terminate while statement")
                    pass

                if(content != None):
                    store = self._db.query(
                        "SELECT * FROM stores WHERE s_ID IN (\"{}\")".format(content))

                    if (len(store) > 0):
                        currentDT = datetime.now().replace(microsecond=0)

                        recorded = self._db.query(
                            "SELECT COUNT(*) FROM customers_health_record WHERE u_ID = {} AND s_ID = {} AND dt_rec BETWEEN \"{}\" AND \"{}\"".format(
                                self._info["uID"], store[0], str(currentDT - timedelta(minutes=10)), str(currentDT)))
                        recorded = recorded[0]

                        if (recorded == 0):
                            self._db.insert("customers_health_record",
                                            ["u_id", "s_id", "dt_rec"], [self._info["uID"], store[0], str(currentDT)])
                            print("Added to Records")
                            system('pause')
                            return True
                        else:
                            print("Already Added")
                    else:
                        print("{} s_id Not found".format(content))
                    system('pause')
                    return False
                else:
                    print("Content is Empty")
            else:
                return False
        except:
            print("Error Reading QR Code (Possible Reason: Camera is Inaccessible")
            system("pause")

    def uploadProof(self, proof):
        '''
            insert the link to the proof to the proof_of_records table 
            Args:
                proof - string, link to the cloud storage the user 
                submitted that contains medical proof of being covid positive
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''

        if (self._isVerified):
            currentDT = datetime.now().replace(microsecond=0)
            latestEntryCount = self._db.query("SELECT COUNT(uploaded_by) FROM proof_records WHERE p_id = {} and dt_uploaded BETWEEN \"{}\" and \"{}\"".format(self._info["uID"],
                                                                                                                                                              str(currentDT - timedelta(hours=1)), str(currentDT)))
            latestEntryCount = latestEntryCount[0]

            if (latestEntryCount == 0):
                self._db.insert("proof_records", ["proofLink", "uploaded_by", "dt_uploaded"], [
                                proof, self._info["uID"], str(datetime.now().replace(microsecond=0))])
                return True

            else:
                print("Already Have an Entry within an Hour Ago")
                return False
        else:
            return False

    def setHealthStatToInfected(self):
        '''
            This will be used in the gui upon the verification of the customer
            if the submitted proof was Accepted, the the health stat will be 'Primary inf'
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''
        if (self._isVerified):
            proof = self._db.query(
                "SELECT DISTINCT * FROM proof_records WHERE uploaded_by = {}".format(self._info["uID"]))
            if (len(proof) > 0):
                if (proof[4] == 'Approved' and proof[5] != None and proof[6] != None):
                    self._info["infCov"] = "Primary Inf"
                    self._db.update("users", ["inf_cov"], [
                                    self._info["infCov"]], "u_id = {}".format(self._info["uID"]))

                return True
            else:
                print("{} uploaded_by Not Found".format(self._info["uID"]))
        else:
            return False

    def getStoreInfo(self, storeID):
        '''
            Returns some general infromation about the store from the passed sID
            Args:
                storeID: int, id of the store to be used for searching the the stores table
            Returns:
                Dictionary containing store information
                    {'sNum': None, 'floor': None, 'wing': None, 'name': None}
                False - certain conditions not met
        '''

        tempStoreInfo = self._db.query(
            "SELECT store_num, floor, wing, name FROM stores WHERE store_num = {}".format(storeID))
        storeInfo = {}

        if (len(tempStoreInfo) > 0):
            storeInfo["sNum"] = tempStoreInfo[0]
            storeInfo["floor"] = tempStoreInfo[1]
            storeInfo["wing"] = tempStoreInfo[2]
            storeInfo["name"] = tempStoreInfo[3]
            return storeInfo
        else:
            print("{} store_num Not Found".format(storeID))
            return False

    def getHistory(self, instances=5):
        '''
            Get the dates the user visted the mall and also the stores they visited on the said date
            Args:
                instances: int, number of dates to get
            Retuns:
                List containing the dates and corresponding vistited store
                    [{'date' : None, 'stores': [{'sNum': None, 'floor': None, 'wing': None, 'name': None}]}]
                False - certain conditions not met
        '''

        history = []
        tempDates = self._db.query(
            "SELECT DISTINCT DATE(dt_rec) FROM customers_health_record WHERE u_id = {} ORDER BY dt_rec DESC LIMIT {}".format(self._info['uID'], instances))

        if (len(tempDates) > 0):
            for d in tempDates:
                log = {"date": None, "stores": []}
                d = str(d)
                log['date'] = d

                tempStores = self._db.query(
                    "SELECT s_id, MAX(TIME(dt_rec)) FROM customers_health_record WHERE DATE(dt_rec) = '{}' AND u_id = {} GROUP BY s_id".format(d, self._info['uID']))

                if (type(tempStores[0]) == int):
                    storeInfo = self.getStoreInfo(tempStores[0])
                    storeInfo["timeEnt"] = str(tempStores[1])
                    log['stores'].append(storeInfo)

                else:
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


class Admin(User):
    def __init__(self, database, qrCodePath="QRcodes/"):
        # prevent overiding of parent's init
        User.__init__(self, database)
        super().__init__(database)  # inherits all methods and properties
        self.__qrCodePath = qrCodePath
        self.contact = Contact(self._db)

    def generateQRCode(self, storeInfo):
        '''
            Generates a qr code containing a store ID
            Args:
                storeInfo: dictionary of store info
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''

        try:
            id_qrCode = qrcode.make(storeInfo["sID"])
            qrName = str(storeInfo["sID"]) + "_" + \
                str(storeInfo["sNum"]) + "_" + storeInfo["name"] + ".jpg"
            id_qrCode.save(self.__qrCodePath + qrName)
            return (self.__qrCodePath + qrName)
        except Exception as e:
            print(e)
            return False

    def newStore(self, p_storeNum, p_floor, p_wing, p_name, p_cNum, p_email):
        '''
            Insert information of new store to the stores table
            Args:
                p_storeNum: int
                p_floor: int
                p_wing: sting
                p_name: sting
                p_cNum: string
                p_email: string
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''

        existingStore = self._db.query(
            "SELECT COUNT(store_num) FROM stores WHERE store_num = {} AND dt_rem IS NULL".format(p_storeNum))

        if(len(existingStore) > 0):
            existingStore = existingStore[0]
        else:
            return False

        if (existingStore == 0):
            self._db.insert("stores", ["store_num", "floor", "wing", "name", "c_num", "email", "dt_add"], [
                            p_storeNum, p_floor, p_wing, p_name, p_cNum, p_email, str(datetime.now().date())])
            return True
        else:
            print("{} store_num Already Exist".format(p_storeNum))
            return False

    def getStoreInfo(self, storeID):
        '''
            Returns all infromation about the store from the passed sID
            Args:
                storeID: int, id of the store to be used for searching the the stores table
            Returns:
                Dictionary containing store information
                    {'sID': None, 'sNum': None, 'floor': None, 'wing': None, 'name': None
                    'cNum': None, 'email': None, 'dt_add': None, 'dt_rem': None}
                False - certain conditions not met
        '''
        tempData = self._db.query(
            "SELECT * FROM stores WHERE store_num = {}".format(storeID))
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
            print("{} store_num Not Found".format(storeID))
            return False

    def getStoresID(self, instances=5):
        '''
            Returns a list of sID
            Arg:
                instances: int, number of sID to return
            Returns:
                List of sID
        '''
        stores = self._db.query(
            "Select s_id FROM stores WHERE dt_rem IS NULL LIMIT {}".format(instances))
        return stores

    def updateStoreInfo(self, sID, cols, values):
        '''
            Updates the information on of the store with the specified store id
            Args:
                sId: int, store id
                cols: the values to be changed
                values: the new value/s
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''
        if "s_id" in cols:
            toRemove = cols.index("s_id")
            del cols[toRemove]
            del values[toRemove]

        numOfExisting = self._db.query(
            "SELECT COUNT(*) FROM stores WHERE store_num = {} AND dt_rem IS NOT NULL".format(sID))

        if (numOfExisting == 0):
            self._db.update("stores", cols, values,
                            "s_id = {}".format(sID))
            return True
        elif(numOfExisting > 0):
            print('Store Number Already Exist')
            return False

    def deleteStore(self, sID):
        '''
            Updates the dt_rem on the store table to the current date
            Args:
                sID: int, id of the store
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''
        currentDTRem = self._db.query(
            "SELECT dt_rem FROM stores WHERE s_id = {}".format(sID))

        if(len(currentDTRem) > 0):
            currentDTRem = currentDTRem[0]
        else:
            return False

        if (currentDTRem == None):
            self._db.update('stores', ["dt_rem"], [
                str(datetime.now().date())], "s_id = {}".format(sID))
            return True
        else:
            print("Already Deleted on {}".format(currentDTRem))
            return False

    def getPendingProof(self, intances=5):
        '''
            Get the list of proofs from proof_records that is awaiting approval from admin
            Args:
                instances: int, number of item to get
            Returns:
                list of dictionary, where dictionary contains the information about the pending proof
        '''
        pending = []
        tempPending = self._db.query(
            "SELECT * FROM proof_records WHERE status = 'Pending' ORDER BY dt_uploaded DESC LIMIT {}".format(intances))

        if (len(tempPending) > 0):

            # [(x,y,z),(x,y,z),(x,y,z)]
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

            #[x, y, z]
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

        # [{},{},{}]
        return pending

    def updateProofStat(self, uID, status):
        '''
            Change the status of proof of request
            Args:
                pID: int the key or id of the said proof
                status: the new status
            Returns:
                True - task perfomed succesfully
                False - certain conditions not met
        '''

        if (status == 'Approved' or status == 'Denied' or status == 'Pending'):
            self._db.update("proof_records", ["status", "stat_changed_by", "dt_stat_changed"], [
                            status, self._info["uID"], str(datetime.now().replace(microsecond=0))], "uploaded_by = {}".format(uID))
            self._db.update("users", ["inf_cov"], [
                            "Primary Inf"], "u_id = {}".format(uID))
            return True
        else:
            return False

    def getCustSampleInfo(self, uID):
        temp = self._db.query(
            "Select u_id, f_name, l_name from users where u_id = {}".format(uID))
        info = {}
        info["uID"] = temp[0]
        info["name"] = temp[1] + " " + temp[2]
        return info

    def getCustInfo(self, uID):
        temp = self._db.query(
            "Select * from users where u_id = {}".format(uID))
        info = {}
        info["uID"] = temp[0]
        info["cNum"] = temp[1]
        info["name"] = temp[5] + " " + temp[6]
        info["age"] = temp[7]
        info["gender"] = temp[8]
        info["address"] = temp[9] + ", " + temp[10] + ", " + temp[11]
        return info
