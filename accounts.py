from user import User
import qrcode
import cv2 as cv
from PIL import Image


class Customer(User):
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


class Admin(User):
    def generateQRCode(self):
        id_qrCode = qrcode.make(self.__info['uID'])
        id_qrCode.save("id_qrCode.jpg")
        pass
