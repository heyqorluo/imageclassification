import modal
from modal import App, web_endpoint
from typing import Dict


App = modal.App("example-get-started")
image = modal.Image.debian_slim().pip_install("tensorflow").copy_local_file("./output/model.h5","model.h5")

@App.function()
@web_endpoint()
def square(x):
    x=int(x)
    return {"square": x**2}

@App.function(image=image,mounts=[modal.Mount.from_local_file("model.h5", "model.h5")])
def predict(image_array):
    # import tensorflow as tf
    from tensorflow.keras import models
    # print(img)
    # image_array= tf.keras.preprocessing.image.img_to_array(img)
    # image_array= tf.keras.preprocessing.image.smart_resize(image_array,(32,32))
    # image_array = tf.expand_dims(image_array, 0)  # Create batch axis
    # image_array /= 255.0  # Normalize
    CLASS_NAMES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
    
    # Load the model
    model = models.load_model("/model.h5", compile=False)
    model.save("/model.h5")
    predictions = model.predict(image_array)
    import numpy as np
    predicted_class = np.argmax(predictions)

    # Sort the predictions
    sorted_indices = np.argsort(predictions, axis=-1)[:, ::-1]
    prediction_result ={}

    # Print the results
    for i in sorted_indices[0]:
        key = CLASS_NAMES[i].ljust(20, ".")
        probability = "{:.1f}".format(predictions[0][i] * 100).rjust(5, " ")
        print(f"{key} : {probability}%")
        prediction_result[key]=probability

    print(f"\n\nPredicted class: {CLASS_NAMES[predicted_class]}")
    
    return {"message": "image received", "prediction_result":prediction_result}