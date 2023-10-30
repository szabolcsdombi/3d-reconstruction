import numpy as np

import utils
from camera import Camera

camera = Camera(size=(320, 240))

captures = [
    camera.capture(position=position, target=target)
    for position, target in [
        [(-1.0, -4.0, 1.0), (0.0, 0.0, 0.0)],
        [(0.0, -4.0, 1.0), (0.0, 0.0, 0.0)],
        [(1.0, -4.0, 1.0), (0.0, 0.0, 0.0)],
    ]
]

points = np.concatenate([
    utils.depth_to_world(
        capture['color_image'],
        capture['depth_image'],
        capture['camera_position'],
        capture['camera_target'] + utils.random_normal_vector(0.05),
        capture['camera_settings'],
    )
    for capture in captures
])

with open('points.obj', 'w') as f:
    f.write(utils.points_to_obj(points))
