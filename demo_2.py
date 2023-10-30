import matplotlib.pyplot as plt

from camera import Camera
import utils

camera = Camera(size=(320, 240))

captures = [
    camera.capture(position=c['camera_position'], target=c['camera_target'])
    for c in utils.random_camera_angles(20)
]

fig, axes = plt.subplots(5, 8)
for i in range(20):
    ax = axes.flatten()[i * 2]
    ax.imshow(captures[i]['color_image'])
    ax.axis('off')
    ax = axes.flatten()[i * 2 + 1]
    ax.imshow(captures[i]['depth_image'])
    ax.axis('off')

plt.show()
