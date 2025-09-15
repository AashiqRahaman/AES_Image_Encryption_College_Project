import os
import pydicom
import numpy as np
import imageio
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def dicom_to_jpeg2000_and_encrypt(input_path, output_folder, password):
    # Load DICOM
    dataset = pydicom.dcmread(input_path)
    pixel_array = dataset.pixel_array

    # Normalize pixel values
    image = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype('uint8')

    # Save as JPEG 2000
    filename = os.path.basename(input_path).replace('.dcm', '.jp2')
    temp_jp2_path = os.path.join(output_folder, filename)
    imageio.imwrite(temp_jp2_path, image, format='jp2')

    # Read image bytes
    with open(temp_jp2_path, 'rb') as f:
        image_data = f.read()

    # AES Encryption
    key = SHA256.new(password.encode()).digest()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

    # Save encrypted image
    enc_path = os.path.join("encrypted_images", filename + ".enc")
    with open(enc_path, 'wb') as f:
        f.write(iv + encrypted_data)

    # Clean up original JPEG 2000
    os.remove(temp_jp2_path)
    print(f"Encrypted file saved: {enc_path}")

Password = input("Enter a Password to lock:-")

# Example usage
if __name__ == "__main__":
    dicom_to_jpeg2000_and_encrypt("dicom_files/sample1.dcm", "decrypted_images", Password)
