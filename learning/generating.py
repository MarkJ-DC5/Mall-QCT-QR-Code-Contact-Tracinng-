import qrcode
import cv2 as cv
from PIL import Image

# for generating Qr Code
img = qrcode.make("Contact Tracing")
img.save("ctracing.jpg")

# for reading Qr Code
det = cv.QRCodeDetector()
val, points, straight_qrcode = det.detectAndDecode(cv.imread("ctracing.jpg"))
