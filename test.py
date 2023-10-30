import matplotlib.pyplot as plt
import numpy as np

from camera import Camera
from utils import random_camera_angles

camera = Camera(size=(1280, 720))

captures = [
    camera.capture(position=c['camera_position'], target=c['camera_target'], fov=c['camera_field_of_view'])
    for c in random_camera_angles(20)
]

fix, ax = plt.subplots(5, 4)
for y in range(5):
    for x in range(4):
        ax[y, x].imshow(captures[y * 4 + x]['color_image'])

plt.show()
