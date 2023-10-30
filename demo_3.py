import matplotlib.pyplot as plt

import utils
from camera import Camera

camera = Camera(size=(320, 240))

capture = camera.capture(position=(1.0, -4.0, 1.0), target=(0.0, 0.0, 0.0))
points = utils.depth_to_world(
    capture['color_image'], capture['depth_image'],
    capture['camera_position'], capture['camera_target'], capture['camera_settings'],
)

with open('points.obj', 'w') as f:
    f.write(utils.points_to_obj(points, eps=0.02))

ax = plt.figure().add_subplot(aspect='equal', projection='3d')
ax.plot(points[:, 0], points[:, 1], points[:, 2], 'b.')
ax.set_xlim3d(-2.0, 2.0)
ax.set_ylim3d(-2.0, 2.0)
ax.set_zlim3d(-2.0, 2.0)
plt.show()
