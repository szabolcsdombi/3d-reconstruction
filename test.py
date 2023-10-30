import matplotlib.pyplot as plt
import numpy as np

from camera import Camera
import utils

camera = Camera(size=(320, 240))

captures = [
    camera.capture(position=c['camera_position'], target=c['camera_target'])
    for c in utils.random_camera_angles(20)
]

points = np.concatenate([
    utils.depth_to_world(
        c['color_image'],
        c['depth_image'],
        c['camera_position'] + utils.random_normal_vector(0.05),
        c['camera_target'] + utils.random_normal_vector(0.05),
        c['camera_settings'],
    )
    for c in captures
])

with open('points.obj', 'w') as f:
    f.write(utils.points_to_obj(points))

# ax = plt.figure().add_subplot(aspect='equal', projection='3d')
# ax.plot(points[:, 0], points[:, 1], points[:, 2], 'b.')
# ax.set_xlim3d(-2.0, 2.0)
# ax.set_ylim3d(-2.0, 2.0)
# ax.set_zlim3d(-2.0, 2.0)
# plt.show()
