import matplotlib.pyplot as plt

from camera import Camera

camera = Camera(size=(1280, 720))

capture = camera.capture(position=(1.0, -4.0, 1.0), target=(0.0, 0.0, 0.0))

fig, ax = plt.subplots(2, 1)
ax[0].imshow(capture['color_image'])
ax[1].imshow(capture['depth_image'])
ax[0].axis('off')
ax[1].axis('off')
plt.show()
