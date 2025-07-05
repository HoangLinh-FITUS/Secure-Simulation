import cv2 
import qrcode
from pyzbar.pyzbar import decode

def create_qr(data, filename: str):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def read_qr(filename: str) -> str:
    img = cv2.imread(filename)
    decoded_objects = decode(img)
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')  
    else:
        raise Exception("No QR code found")
