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
