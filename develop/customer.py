from user import *


class Customer(User):
    def generateQRCode(self):
        id_qrCode = qrcode.make(self.info['uID'])
        id_qrCode.save("id_qrCode.jpg")


cust1 = Customer()
# cust1.newUser("0956", "secret", 'F', "Mark", "F",
#               "DC", 19, 'M', "398", "X", "Y", "Z")

# print(cust1.verifyUser("0956", "secret"))
# print(cust1.info)
# cust1.generateQRCode()
