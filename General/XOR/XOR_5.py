from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

img1 = Image.open("lemur.png").convert("RGB")
img2 = Image.open("flag.png").convert("RGB")

img1 = np.array(img1)
img2 = np.array(img2)
plt.imshow(img1^img2)
plt.show()