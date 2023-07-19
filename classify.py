import base64
import json

import requests
from PIL import Image

# url = 'http://127.0.0.1:8000/classify_image'
url = 'https://upx3yb0685.execute-api.eu-west-2.amazonaws.com/api/classify_image'
image_file = 'dog.jpeg'

with open(image_file, "rb") as f:
    im_bytes = f.read()
im_b64 = base64.b64encode(im_bytes).decode("utf8")

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

payload = json.dumps({"image": im_b64})
response = requests.post(url, data=payload, headers=headers)
try:
    data = response.json()
    print(data)
except requests.exceptions.RequestException:
    print(response.text)
