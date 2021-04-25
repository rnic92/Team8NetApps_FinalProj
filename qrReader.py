import qrcode
import cv2
import time

def generate_qr(name):
    randtag = str(time.time()) + name
    filename = "testfile.png"
    img = qrcode.make(randtag)
    img.save(filename)
    return randtag

def read_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        ret,frame = cap.read()
        data, bbox, straight_qrcode = detector.detectAndDecode(frame)
        if straight_qrcode is not None:
            return data
            cap.release()
            cv2.destroyAllWindows()
            break;

if __name__ == '__main__':
    img = generate_qr("nicolas")
    read_qr()
