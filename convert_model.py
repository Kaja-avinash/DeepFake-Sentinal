from keras.models import load_model
import tensorflow as tf

model = load_model("models/deepfake_mobilenet_finetuned.h5", compile=False)

model.save("models/final_model")

print("CONVERSION COMPLETE")
