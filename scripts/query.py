#upload local image
import numpy as np
import os
import sys
import tensorflow as tf
import modal

def read_command_line_arguments():
    if len(sys.argv) != 2:
        print("Expected 1 argument, but received", len(sys.argv) - 1)
        print("Use: python run.py <path/to/image.png>")
        exit()

    input_filepath = sys.argv[1]
    return input_filepath


def load_image(input_filepath):
    image = tf.keras.preprocessing.image.load_img(input_filepath, target_size=(32, 32))
    print(image) #<PIL.Image.Image image mode=RGB size=32x32 at 0x1A61C80C1C0>
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    # print(image_array.shape) (32,32,3)
    image_array = tf.expand_dims(image_array, 0)  # Create batch axis
    image_array /= 255.0  # Normalize
    return image_array


if __name__ == "__main__":
    # Get the input filepath
    input_filepath = read_command_line_arguments()

    # Sample image
    image_array = load_image(input_filepath)
    
    #using modal
    modal_function = modal.Function.lookup("example-get-started","predict")
    result = modal_function.call(image_array)
    print(result)