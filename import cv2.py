import cv2
import numpy as np
import urllib.request

url='http://192.168.110.193/cam-lo.jpg'

while True:
    imgResponse = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
    img = cv2.imdecode(imgnp,-1)

    flip = cv2.flip(img,-1) # flip gambar

    cv2.imshow('FRAME',flip)
    if cv2.waitKey(1) == ord('q'):
        break
        
url.release()
cv2.destroyAllWindows()