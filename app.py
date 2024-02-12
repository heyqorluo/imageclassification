from chalice import Chalice,  Response, CORSConfig
import modal
import numpy as np
from PIL import Image

import io                  
import base64              
import json    

app = Chalice(app_name='imageclassification')
app.api.binary_types =['*/*']
cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['*'],
    allow_credentials=True
)

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/classify_image2', methods=['POST'], cors=True, content_types=['application/json'])
def classify_img2():
    body = app.current_request.json_body
    image_b64 = body.get('image')
    image_data = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    img = image.resize((32,32))
    # print(img.shape)
    image_array = np.asarray(img, dtype=np.float32) / 255  # Normalize
    image_array = np.expand_dims(image_array, axis=0)
    print(image_array.shape)
    
    #using modal
    modal_function = modal.Function.lookup("example-get-started","predict")
    result = modal_function.remote(image_array)


    return Response(body={'Result:': result},
                    status_code=200,
                    headers={'Content-Type': 'application/json'}
                  )
    

@app.route('/classify_image', methods=['POST'], cors=True, content_types=['application/json; charset=utf-8', 'application/json'])
def classify_img():
    # request = app.current_request

    # # get the base64 encoded string
    # im_b64 = request.json_body['image']
    
    # Convert the JSON string to a dictionary.
    data = json.loads(app.current_request.json_body)
    # print("\nDATA:\n", data, "\n")

    #Access the 'image' key from the JSON data.
    im_b64 = data['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))
    # print(img_bytes)
    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img = img.resize((32,32))
    image_array = np.asarray(img, dtype=np.float32) / 255  # Normalize
    image_array = np.expand_dims(image_array, axis=0)
    # print(image_array.shape)
    
    #using modal
    modal_function = modal.Function.lookup("example-get-started","predict")
    result = modal_function.remote(image_array)


    return Response(body={'Result:': result},
                    status_code=200,
                    headers={'Content-Type': 'application/json'}
                  )
    
@app.route('/text_test',methods=['POST'], cors=True, content_types=['application/json; charset=utf-8', 'application/json'])
def sending_text():
    request = app.current_request
    print("method:", request.method)
    print("request:", request.raw_body)
    return request.raw_body

#locally working 
#run chalice local and then curl http://127.0.0.1:8000/send_image
@app.route('/send_image', methods=['GET'], content_types=['application/json'])
def serve_img():
    # with open('test.png', 'rb') as img:
    #     img_data = img.read()

    # if not img_data:
    #     raise BadRequestError('Error')
    img = Image.open('dog.jpeg').convert('RGB')
    img = img.resize((32,32))
    image_array = np.asarray(img, dtype=np.float32) / 255  # Normalize
    image_array = np.expand_dims(image_array, axis=0)
    # print(image_array.shape)
    
    #using modal
    modal_function = modal.Function.lookup("example-get-started","predict")
    result = modal_function.remote(image_array)


    return Response(body={'Result:': result},
                    status_code=200,
                    headers={'Content-Type': 'application/json'}
                  )
    # return {'Result:': result}



