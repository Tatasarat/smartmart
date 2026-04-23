import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Load pretrained model
model = MobileNetV2(weights='imagenet')

def predict_trust(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded = decode_predictions(preds, top=1)[0][0]

    confidence = float(decoded[2]) * 100  # confidence %

    return {
        "label": decoded[1],
        "confidence": confidence
    }