import PIL.Image
import pyzbar.pyzbar

img = PIL.Image.open("qrcode.png")
data = pyzbar.pyzbar.decode(img)
cert = data[0].data.decode()
print(cert)
