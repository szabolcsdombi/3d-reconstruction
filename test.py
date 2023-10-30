import matplotlib.pyplot as plt
import numpy as np

from camera import Camera

camera = Camera((512, 512))

capture = camera.capture(position=(2.0, -4.0, 1.0), target=(0.0, 0.0, 0.0), fov=45.0)

plt.imshow(capture['color_image'])
# plt.imshow(depth)
plt.show()
