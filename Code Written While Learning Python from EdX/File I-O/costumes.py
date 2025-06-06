import sys
import time


time.sleep(2)
from PIL import Image

images = []

for arg in sys.argv[1:]:
    image = Image.open(arg)
    images.append(image)
    
images[0].save(
    "costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0
)

# in the terminal write python costumes.py costume1.gif costume2.gif
# code costumes.gif

time.sleep(2)