import numpy as np

import utils
from camera import Camera

camera = Camera(size=(320, 240))

captures = [
    camera.capture(position=c['camera_position'], target=c['camera_target'])
    for c in utils.random_camera_angles(20)
]

points = np.concatenate([
    utils.depth_to_world(
        capture['color_image'],
        capture['depth_image'],
        capture['camera_position'],
        capture['camera_target'],
        capture['camera_settings'],
    )
    for capture in captures
])

with open('points.obj', 'w') as f:
    f.write(utils.points_to_obj(points, eps=0.005))
