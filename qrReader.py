import qrcode
import cv2
import time
"""
Idea on how to generate and read QR codes inspired from
https://www.thepythoncode.com/article/generate-read-qr-code-python

Appreciation to Abdou Rockikz
"""
def generate_qr(name):
    filename = "testfile.png"
    img = qrcode.make(name)
    img.save(filename)
    return name

def read_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    print("[Client 03] – Waiting to scan Username QR Code")
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
