import numpy as np
import matplotlib.pyplot as plt

def view_encrypted_image_as_noise(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # Convert to numpy array of 8-bit unsigned integers
    data_np = np.frombuffer(data, dtype=np.uint8)

    # Reshape to square or near-square 2D array
    side = int(np.ceil(np.sqrt(len(data_np))))
    padded_length = side * side
    data_np = np.pad(data_np, (0, padded_length - len(data_np)), mode='constant')

    image = data_np.reshape((side, side))

    # Display as grayscale "encrypted" noise image
    plt.imshow(image, cmap='gray')
    plt.title("Encrypted Image Visualized as Noise")
    plt.axis('off')
    plt.show()



view_encrypted_image_as_noise("sample1.jp2.enc")
