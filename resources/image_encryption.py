import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2

# Load and preprocess image
def load_image(path, size=(256, 256)):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, size)
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=-1)  # Add channel dimension
    return img

# Encoder model
def build_encoder(input_shape):
    inputs = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.MaxPooling2D(2)(x)
    encoded = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
    return models.Model(inputs, encoded, name="encoder")

# Decoder model
def build_decoder(encoded_shape):
    inputs = layers.Input(shape=encoded_shape)
    x = layers.Conv2DTranspose(64, 3, strides=2, activation='relu', padding='same')(inputs)
    x = layers.Conv2DTranspose(32, 3, strides=2, activation='relu', padding='same')(x)
    decoded = layers.Conv2D(1, 3, activation='sigmoid', padding='same')(x)
    return models.Model(inputs, decoded, name="decoder")

# Generate chaotic key (simple logistic map example)
def logistic_map(size, x0=0.5, r=3.99):
    x = x0
    key = []
    for _ in range(size):
        x = r * x * (1 - x)
        key.append(x)
    return np.array(key)

# Example of training loop (simplified)
def train_autoencoder(encoder, decoder, images, epochs=50):
    optimizer = tf.keras.optimizers.Adam()
    mse = tf.keras.losses.MeanSquaredError()

    for epoch in range(epochs):
        for img in images:
            img = np.expand_dims(img, axis=0)  # batch size 1
            with tf.GradientTape() as tape:
                encoded = encoder(img)
                # Here, combine encoded features with chaotic key if needed
                decoded = decoder(encoded)
                loss = mse(img, decoded)
            grads = tape.gradient(loss, encoder.trainable_variables + decoder.trainable_variables)
            optimizer.apply_gradients(zip(grads, encoder.trainable_variables + decoder.trainable_variables))
        print(f"Epoch {epoch+1}, Loss: {loss.numpy()}")

# Usage
image = load_image('medical_image.png')
encoder = build_encoder(image.shape)
decoder = build_decoder(encoder.output_shape[1:])
train_autoencoder(encoder, decoder, [image])
