import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os

# 1. Create the 'models' folder if it doesn't exist
if not os.path.exists("models"):
    os.makedirs("models")
    print("✅ Created 'models' folder.")

print("⏳ Generating a placeholder model... (This takes a few seconds)")

# 2. Build the Model Architecture (MobileNetV2)
base_model = MobileNetV2(
    weights="imagenet", include_top=False, input_shape=(224, 224, 3)
)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
predictions = Dense(1, activation="sigmoid")(x)
model = Model(inputs=base_model.input, outputs=predictions)

# 3. Compile the model (Dummy compilation to allow saving)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 4. Save the model file
save_path = os.path.join("models", "final_model")
model.save(save_path)

print(f"🎉 SUCCESS! Model saved at: {save_path}")
print("👉 You can now run 'streamlit run src/app.py'")
