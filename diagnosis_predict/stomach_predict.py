import os
import sys
from PIL import Image

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dense, Flatten, Activation

# Some utilites
import numpy as np


# function of prediction
def model_predict(img, model):
    # shaping the image
    img = img.resize((250, 300))
    img = img.convert("RGB")

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x, mode='tf')

    # getting results
    preds = model.predict(x)
    print(preds)

    return preds


def disease(x):
    return {
        0: 'dyed-lifted-polyps',
        1: 'esophagitis',
        2: 'normal-cecum'
    }.get(x, 'ERROR')


def predict_category(image_path):
    # setting path to model-file
    model_path = "C:\\Users\\aleks\\PycharmProjects\\GUI\\diagnosis_predict\\stomachFin.h5"

    # loading model
    model = keras.models.load_model(model_path)

    # print model's info into terminal
    # model.summary()
    # loading image to analysis
    # image_origin = Image.open(sys.argv[1])
    image_origin = Image.open(image_path)
    # getting prediction results
    predictions = model_predict(image_origin, model)

    # processing predictions results
    result_number = np.argmax(predictions).__int__()
    result_string = disease(result_number)

    # saving result
    with open('result_prediction', 'w+') as file:
        file.write(result_string)

    print("Done working.")
    print("Dobby can be free :')")
    return os.path.abspath("result_prediction")
