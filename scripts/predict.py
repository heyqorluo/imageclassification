from tensorflow.keras import models
import numpy as np
import os
import sys
import tensorflow as tf

# Settings
MODEL_NAME = "model"
CLASS_NAMES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]


def read_command_line_arguments():
    if len(sys.argv) != 2:
        print("Expected 1 argument, but received", len(sys.argv) - 1)
        print("Use: python run.py <path/to/image.png>")
        exit()

    input_filepath = sys.argv[1]
    return input_filepath


def load_image(input_filepath):
    image = tf.keras.preprocessing.image.load_img(input_filepath, target_size=(32, 32))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)  # Create batch axis
    image_array /= 255.0  # Normalize
    return image_array


if __name__ == "__main__":
    # Get the input filepath
    input_filepath = read_command_line_arguments()

    # Load the image
    image = tf.keras.preprocessing.image.load_img(input_filepath, target_size=(32, 32))

    # Load the model
    model = models.load_model(os.path.join("output", f"{MODEL_NAME}.h5"))

    # Sample image
    image_array = load_image(input_filepath)
    predictions = model.predict(image_array)
    predicted_class = np.argmax(predictions)

    # Sort the predictions
    sorted_indices = np.argsort(predictions, axis=-1)[:, ::-1]

    # Print the results
    for i in sorted_indices[0]:
        key = CLASS_NAMES[i].ljust(20, ".")
        probability = "{:.1f}".format(predictions[0][i] * 100).rjust(5, " ")
        print(f"{key} : {probability}%")

    print(f"\n\nPredicted class: {CLASS_NAMES[predicted_class]}")