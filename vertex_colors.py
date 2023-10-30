import gzip
import struct

import numpy as np
import zengl

zengl.init(zengl.loader(headless=True))
ctx = zengl.context()

size = (512, 512)
image = ctx.image(size, 'rgba8unorm')
depth = ctx.image(size, 'depth32float')

model = gzip.decompress(open('colormonkey.mesh.gz', 'rb').read())
vertex_buffer = ctx.buffer(model)

uniform_buffer = ctx.buffer(size=96)

pipeline = ctx.pipeline(
    vertex_shader='''
        #version 300 es
        precision highp float;

        layout (std140) uniform Common {
            mat4 mvp;
            vec4 eye_pos;
            vec4 light_pos;
        };

        layout (location = 0) in vec3 in_vertex;
        layout (location = 1) in vec3 in_normal;
        layout (location = 2) in vec3 in_color;

        out vec3 v_vertex;
        out vec3 v_normal;
        out vec3 v_color;

        void main() {
            v_vertex = in_vertex;
            v_normal = in_normal;
            v_color = in_color;
            gl_Position = mvp * vec4(v_vertex, 1.0);
        }
    ''',
    fragment_shader='''
        #version 300 es
        precision highp float;

        layout (std140) uniform Common {
            mat4 mvp;
            vec4 eye_pos;
            vec4 light_pos;
        };

        in vec3 v_vertex;
        in vec3 v_normal;
        in vec3 v_color;

        const vec3 light_color = vec3(1.0, 1.0, 1.0);
        const float light_power = 20.0;

        layout (location = 0) out vec4 out_color;

        vec3 blinn_phong() {
            float ambient = 0.2;
            float facing = 0.1;
            float shininess = 16.0;

            vec3 light_dir = light_pos.xyz - v_vertex;
            float light_distance = length(light_dir);
            light_distance = light_distance * light_distance;
            light_dir = normalize(light_dir);

            float lambertian = max(dot(light_dir, v_normal), 0.0);
            float specular = 0.0;

            vec3 view_dir = normalize(eye_pos.xyz - v_vertex);

            if (lambertian > 0.0) {
                vec3 half_dir = normalize(light_dir + view_dir);
                float spec_angle = max(dot(half_dir, v_normal), 0.0);
                specular = pow(spec_angle, shininess);
            }

            float facing_view_dot = max(dot(view_dir, v_normal), 0.0);

            vec3 color_linear = v_color * ambient + v_color * facing_view_dot * facing +
                v_color * lambertian * light_color.rgb * light_power / light_distance +
                specular * light_color.rgb * light_power / light_distance;

            vec3 color_gamma_corrected = pow(color_linear, vec3(1.0 / 2.2));
            return color_gamma_corrected;
        }

        void main() {
            out_color = vec4(blinn_phong(), 1.0);
        }
    ''',
    layout=[
        {
            'name': 'Common',
            'binding': 0,
        },
    ],
    resources=[
        {
            'type': 'uniform_buffer',
            'binding': 0,
            'buffer': uniform_buffer,
        },
    ],
    framebuffer=[image, depth],
    topology='triangles',
    cull_face='back',
    vertex_buffers=zengl.bind(vertex_buffer, '3f 3f 3f', 0, 1, 2),
    vertex_count=vertex_buffer.size // zengl.calcsize('3f 3f 3f'),
)

t = 10.0

ctx.new_frame()
light = (3.0, -4.0, 10.0)
eye = (np.cos(t * 0.5) * 5.0, np.sin(t * 0.5) * 5.0, 1.0)
camera = zengl.camera(eye, (0.0, 0.0, 0.0), aspect=size[0] / size[1], fov=45.0)
uniform_buffer.write(struct.pack('64s3f4x3f4x', camera, *eye, *light))

image.clear()
depth.clear()
pipeline.render()
ctx.end_frame()

import matplotlib.pyplot as plt
import numpy as np

plt.imshow(np.frombuffer(image.read(), 'u1').reshape(size[1], size[0], 4))
plt.show()
