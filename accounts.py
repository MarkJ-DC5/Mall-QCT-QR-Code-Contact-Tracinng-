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


class Admin(User):
    def __init__(self, database, qrCodePath="QRcodes/"):
        # prevent overiding of parent's init
        User.__init__(self, database)
        super().__init__(database)  # inherits all methods and properties
        self.__qrCodePath = qrCodePath

    def getStoreInfo(self, storeNum):
        data = self._db.query(
            "SELECT * FROM stores WHERE store_num = {}".format(storeNum))
        if (data != False):
            if (len(data) > 0):
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
