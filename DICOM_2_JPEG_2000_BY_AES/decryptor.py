from PIL import Image
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad


def decrypt_image(enc_file, output_folder, password):
    with open(enc_file, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    key = SHA256.new(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    output_filename = os.path.basename(enc_file).replace('.jp2.enc', '_decrypted.jp2')
    output_path = os.path.join(output_folder, output_filename)

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
    print(f"Decrypted image saved: {output_path}")
    
Password = input("Enter the Password to Unlock:-")

# Example usage
if __name__ == "__main__":
    decrypt_image("encrypted_images/sample1.jp2.enc", "decrypted_images", Password)
    img = Image.open("decrypted_images/sample1_decrypted.jp2")
    img.save("output.png")
