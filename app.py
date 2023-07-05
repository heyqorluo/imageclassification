from chalice import Chalice

app = Chalice(app_name='imageclassification')


@app.route('/{a}/{b}')
def index(a,b):
    a= int(a)
    b= int(b)
    return a+b

