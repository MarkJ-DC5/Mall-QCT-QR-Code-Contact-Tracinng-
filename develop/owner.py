from user import *


class Owner(User):
    def readQR(self, img):
        try:
            val, points, straight_qrcode = cv.QRCodeDetector().detectAndDecode(cv.imread(img))
            try:
                data = self._db.query(
                    "SELECT * FROM Users WHERE u_ID IN (\"{}\")".format(val))
                return data
            except Exception as e:
                print(e)
                print("Error Retriving Data")
        except:
            print("Error in Reading QR Code")


own1 = Owner()
print(own1.readQR("id_qrCode.jpg"))
