import requests
import cv2
import numpy as np


def cat_http_code(status_code, url):
    if status_code != 200:
        print(url)
        root_url = "https://http.cat/"
        cat_url = root_url + str(status_code)
        resp = urllib.request.urlopen(cat_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        sys.exit(1)
    else:
        pass
