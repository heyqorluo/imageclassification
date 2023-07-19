import requests 
url = 'https://heyqorluo--example-get-started-predict.modal.run'
data = {'media':0}

r = requests.post(url, data=data)
print(r)