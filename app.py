from chalice import Chalice,  Response
import modal
import numpy as np
from PIL import Image

import io                  
import base64                  

app = Chalice(app_name='imageclassification')
app.api.binary_types =['*/*']

@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/classify_image', methods=['POST'])
def classify_img():
    request = app.current_request

    # get the base64 encoded string
    im_b64 = request.json_body['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    # img = Image.open(io.BytesIO(img_bytes))

    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img = img.resize((32,32))
    image_array = np.asarray(img, dtype=np.float32) / 255  # Normalize
    image_array = np.expand_dims(image_array, axis=0)
    # print(image_array.shape)
    
    #using modal
    modal_function = modal.Function.lookup("example-get-started","predict")
    result = modal_function.call(image_array)


    return Response(body={'Result:': result},
                    status_code=200,
                    headers={'Content-Type': 'application/json'}
                  )
    
@app.route('/text_test',methods=['POST'])
def sending_text():
    request = app.current_request
    print("method:", request.method)
    print("request:", request.raw_body)
    return None

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
    result = modal_function.call(image_array)


    return Response(body={'Result:': result},
                    status_code=200,
                    headers={'Content-Type': 'application/json'}
                  )
    # return {'Result:': result}

# @app.route('/my_route', methods= ['GET'])
# def serve_img():
#     with open('test.png', 'rb') as img:
#         img_data = img.read()

#     if not img_data:
#         raise BadRequestError('Error')
#         #using modal
#     modal_function = modal.Function.lookup("example-get-started","predict")
#     result = modal_function.call(img_data)
#     print(result)


#     return Response(body=result,
#                     status_code=200,
#                     headers={'Content-Type': 'image/jpg'}
#                   )
    
    




# @app.route('/upload', methods=['POST'])
# def upload_image():
#     file = app.current_request.raw_body
#     return {'message': 'Image uploaded successfully'}

