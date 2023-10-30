import numpy as np
import zengl


def random_normal_vector(length):
    while True:
        xyz = np.random.uniform(-1.0, 1.0, 3)
        norm = np.linalg.norm(xyz)
        if norm < 1.0:
            return xyz * length / norm


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


def depth_to_world(color_image, depth_image, camera_position, camera_target, camera_settings):
    camera = zengl.camera(camera_position, camera_target, **camera_settings)
    camera_matrix = np.frombuffer(camera, 'f4').reshape(4, 4).T.copy()
    inv = np.linalg.inv(camera_matrix)

    height, width = depth_image.shape
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


def point_to_mesh(point):
    e = 0.005
    x, y, z, r, g, b = point
    lines = []
    lines.append(f'v {x:.4f} {y:.4f} {z - e:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append(f'v {x + e:.4f} {y:.4f} {z:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append(f'v {x:.4f} {y + e:.4f} {z:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append(f'v {x - e:.4f} {y:.4f} {z:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append(f'v {x:.4f} {y - e:.4f} {z:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append(f'v {x:.4f} {y:.4f} {z + e:.4f} {r:.4f} {g:.4f} {b:.4f}')
    lines.append('f -6 -4 -5')
    lines.append('f -6 -3 -4')
    lines.append('f -6 -2 -3')
    lines.append('f -6 -5 -2')
    lines.append('f -5 -4 -1')
    lines.append('f -4 -3 -1')
    lines.append('f -3 -2 -1')
    lines.append('f -2 -5 -1')
    return '\n'.join(lines)


def points_to_obj(points):
    lines = []
    lines.append('o points')
    for p in points:
        lines.append(point_to_mesh(p))
    return '\n'.join(lines)
