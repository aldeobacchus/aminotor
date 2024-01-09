import tensorflow as tf
from keras.utils import img_to_array
import numpy as np
import os

# Parameters
model_path = os.path.join(os.getcwd(), "model_ki_s")
images_dir_path = os.path.join(os.getcwd(), "images")
nb_images = 10
image_width, image_height = 128, 128


def load_process_images(_image_dir_path, _nb_images):
    # Load and preprocess the images
    images = []
    filenames = os.listdir(_image_dir_path)[:_nb_images]
    for filename in filenames:
        if filename.endswith(".jpg"):
            # Load and resize the image
            img_path = os.path.join(_image_dir_path, filename)
            img = tf.keras.utils.load_img(img_path, target_size=(image_width, image_height))
            img_array = img_to_array(img)
            # Preprocess the image (you may need to adapt this based on your specific requirements)
            img_array = img_array / 255.0  # Normalize pixel values to [0, 1]

            # Append the image and label to the lists
            images.append(img_array)

    return np.array(images)


def load_process_predict(_model_path=model_path, _image_dir_path=images_dir_path, _nb_images=None):
    # Load the model
    model = tf.keras.models.load_model(_model_path)

    if not _nb_images:
        _nb_images = len(os.listdir(_image_dir_path))

    images = load_process_images(_image_dir_path, _nb_images)

    labels_predicted = model.predict(images)

    return np.round(labels_predicted)


#for v in load_process_predict():
# print(v)