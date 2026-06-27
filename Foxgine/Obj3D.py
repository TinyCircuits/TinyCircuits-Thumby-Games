import ujson
from thumbyGrayscale import display
from math import *

class Object3D:
    def __init__(self, fileObjs, model_name, pos, rendType):
        self.models = fileObjs
        self.model_name = model_name
        self.pos = pos
        self.vert_list = []
        self.screen_coords = []
        self.rendType = rendType
        self.skip = 0

    def render(self, fov, w_h, center, cam, min_depth, max_depth):
        verts = self.models[self.model_name]["Verticies"]
        faces = self.models[self.model_name]["Polygons"]

        self.vert_list.clear()
        self.screen_coords.clear()

        for x, y, z in verts:
            x += self.pos[0]
            y += self.pos[1]
            z += self.pos[2]

            x, z = rotate2D((x - cam.pos[0], z - cam.pos[2]), cam.rot[1])
            y, z = rotate2D((y - cam.pos[1], z), cam.rot[0])

            if z == 0:
                z += 0.01

            f = fov / z
            x, y = x * f, y * f
            self.screen_coords.append((center[0] + int(x), center[1] - int(y), z))
            self.vert_list.append((x, y, z))

        for face in faces:
            if len(face) < 4:
                continue

            color = face[-2]
            cull_flag = face[-1]
            
            face1 = face[:3]
            face2 = [face[0], face[2], face[3]]
            
            def process_face(face_part):
                vertices = [self.screen_coords[i] for i in face_part]

                if cull_flag == 1:
                    v0 = self.vert_list[face_part[0]]
                    v1 = self.vert_list[face_part[1]]
                    v2 = self.vert_list[face_part[2]]
                    normal = compute_normal(v0, v1, v2)
                    if normal[2] >= 0:
                        return

                on_screen = all(min_depth < self.vert_list[i][2] < max_depth and
                                -150 <= vertices[i][0] < (w_h[0] + 100) and
                                -150 <= vertices[i][1] < (w_h[1] + 100) for i in range(3))

                if on_screen:
                    if self.rendType == 0:
                        self.draw_edges(vertices, color)
                    if self.rendType == 1:
                        self.fill_polygon(vertices, color)

            process_face(face1)
            if len(face) > 5:
                process_face(face2)

    def draw_edges(self, vertices, color):
        for i in range(len(vertices)):
            x0, y0, _ = vertices[i]
            x1, y1, _ = vertices[(i + 1) % len(vertices)]
            self.draw_line(x0, y0, x1, y1, color)

    def fill_polygon(self, vertices, color):
        vertices = sorted(vertices, key=lambda v: v[1])
    
        if len(vertices) < 3:
            return
    
        min_y = max(int(vertices[0][1]), 0)
        max_y = min(int(vertices[-1][1]), display.height - 1)
    
        for y in range(min_y, max_y, 2):
            intersections = []
            
            for i in range(len(vertices)):
                x1, y1, _ = vertices[i]
                x2, y2, _ = vertices[(i + 1) % len(vertices)]
    
                if y1 <= y < y2 or y2 <= y < y1:
                    if y2 != y1:
                        x_inter = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        intersections.append(x_inter)
    
            if len(intersections) < 2:
                continue
    
            intersections.sort()
            for j in range(0, len(intersections), 2):
                x_start = max(int(intersections[j]), 0)
                x_end = min(int(intersections[j + 1]), display.width - 1)
                for x in range(x_start, x_end, 1):
                    display.setPixel(x, y, color)

    def draw_line(self, x0, y0, x1, y1, color):
        display.drawLine(int(x0), int(y0), int(x1), int(y1), color)

    def distance_from_player(self, player_pos):
        dx = self.pos[0] - player_pos[0]
        dz = self.pos[2] - player_pos[2]
        return sqrt(dx * dx + dz * dz)

def rotate2D(pos, rad):
    x, y = pos
    s, c = sin(rad), cos(rad)
    return x * c - y * s, y * c + x * s

def compute_normal(v0, v1, v2):
    u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    normal = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return normal
