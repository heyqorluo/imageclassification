import requests 
from PIL import Image

url = 'http://127.0.0.1:8000/text_test'


data = "hello"
r = requests.post(url, data=data)
print(r)