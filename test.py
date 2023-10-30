import matplotlib.pyplot as plt
import numpy as np

from camera import Camera
import utils

camera = Camera(size=(320, 240))
c = camera.capture(position=(1.0, -4.0, 1.0), target=(0.0, 0.0, 0.0), fov=45.0)

points = utils.depth_to_world(c['depth_image'], c['camera_matrix'])
print(points)

# plt.imshow(c['depth_image'])
ax = plt.figure().add_subplot(aspect='equal', projection='3d')
ax.plot(points[:, 0], points[:, 1], points[:, 2], 'b.')
ax.set_xlim3d(-2.0, 2.0)
ax.set_ylim3d(-2.0, 2.0)
ax.set_zlim3d(-2.0, 2.0)
plt.show()
