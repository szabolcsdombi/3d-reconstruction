import numpy as np


def random_camera_angles(count):
    res = []

    for _ in range(count):
        r = np.random.uniform(3.0, 6.0)
        u = np.random.uniform(0.0, np.pi * 2.0)
        v = np.random.uniform(-0.2, 0.2)
        position = np.array([np.cos(u) * np.cos(v), np.sin(u) * np.cos(v), np.sin(v)]) * r

        r = np.random.uniform(0.0, 1.0)
        u = np.random.uniform(0.0, np.pi * 2.0)
        v = np.random.uniform(-1.5, 1.5)
        target = np.array([np.cos(u) * np.cos(v), np.sin(u) * np.cos(v), np.sin(v)]) * r

        fov = 45.0

        res.append({
            'camera_position': position.tolist(),
            'camera_target': target.tolist(),
            'camera_field_of_view': float(fov),
        })

    return res


def depth_to_world(color_image, depth_image, camera_matrix):
    height, width = depth_image.shape
    inv = np.linalg.inv(camera_matrix)
    y = np.linspace(1.0, -1.0, height)
    x = np.linspace(-1.0, 1.0, width)
    res = []
    for iy in range(height):
        for ix in range(width):
            if depth_image[iy, ix] > 0.9995:
                continue
            v = np.array([x[ix], y[iy], depth_image[iy, ix] * 2.0 - 1.0, 1.0])
            v = inv @ v
            point = v[:3] / v[3]
            color = color_image[iy, ix].astype('f4') / 255.0
            res.append([*point, *color])
    return np.array(res)


def points_to_obj(points):
    lines = []
    lines.append('o points')
    for x, y, z, r, g, b in points:
        lines.append(f'v {x:.4f} {y:.4f} {z:.4f} {r:.4f} {g:.4f} {b:.4f}')
    return '\n'.join(lines)
