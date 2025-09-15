from PIL import Image

img = Image.open("decrypted_images/sample1_decrypted.jp2")
img.save("output.png")
