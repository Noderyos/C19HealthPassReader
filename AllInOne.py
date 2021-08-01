import PIL.Image
import pyzbar.pyzbar
import zlib
import pprint
import cbor2
import base45
from typing import Union

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
chars_dic = {v: i for i, v in enumerate(chars)}

def b45decode(s: Union[bytes, str]) -> bytes:
  if isinstance(s, str):
    buf = [chars_dic[c] for c in s.strip()]
  else:
    buf = [chars_dic[c] for c in s.decode()]
  buffer_length = len(buf)
  result = []
  for i in range(0, buffer_length, 3):
    if buffer_length - i >= 3:
      x = buf[i] + buf[i + 1] * 45 + buf[i + 2] * 45 * 45
      result.extend(divmod(x, 256))
    else:
      x = buf[i] + buf[i + 1] * 45
      result.append(x)
  return bytes(result)

img = PIL.Image.open(input("QRCode file name :"))
data = pyzbar.pyzbar.decode(img)
cert = data[0].data.decode()
print("RAW Content : " + cert)
b45data = cert
b45data = b45data.replace("HC1:","")
zlibdata = base45.b45decode(b45data)
cbordata = zlib.decompress(zlibdata)
decoded = cbor2.loads(cbordata)
print("Header\n----------------\n")
pprint.pprint(cbor2.loads(decoded.value[0]))
print("\nPayload\n----------------\n");
pprint.pprint(cbor2.loads(decoded.value[2]))
print("\nSignature ?\n----------------\n");
print(decoded.value[3])
