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
                vert_coords = [self.models[self.model_name]["Verticies"][i] for i in face_part]

                if self.check_collision(vertices, cam.pos):
                    cam.changeToLast()
                
                if cull_flag == 1:
                    v0 = self.vert_list[face_part[0]]
                    v1 = self.vert_list[face_part[1]]
                    v2 = self.vert_list[face_part[2]]
                    normal = compute_normal(v0, v1, v2)
                    if normal[2] >= 0:
                        return

                clipped_vertices = [self.vert_list[i] for i in face_part]
                clipped_vertices, screen_vertices = self.clip_polygon(clipped_vertices, vertices, fov)

                if len(clipped_vertices) < 3:
                    return

                on_screen = all(min_depth < v[2] < max_depth and
                                -150 <= sv[0] < (w_h[0] + 100) and
                                -150 <= sv[1] < (w_h[1] + 100) for v, sv in zip(clipped_vertices, screen_vertices))

                if on_screen:
                    if self.rendType == 0:
                        self.draw_edges(screen_vertices, color)
                    if self.rendType == 1:
                        self.fill_polygon(screen_vertices, color)

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

    def check_collision(self, face_part, player_pos):
        player_box = get_bounding_box([player_pos])
        triangle_box = get_bounding_box([face_part])

        if not aabb_collision(player_box, triangle_box):
            return False
        
        player_pos_3d = (player_pos[0], player_pos[1], 0)
        result = point_in_triangle_3d(player_pos_3d, face_part[0], face_part[1], face_part[2])

        return result

    def distance_from_player(self, player_pos):
        dx = self.pos[0] - player_pos[0]
        dz = self.pos[2] - player_pos[2]
        return sqrt(dx * dx + dz * dz)

    def clip_polygon(self, vertices, screen_coords, fov):
        near_plane = 0.01
        clipped_vertices = []
        clipped_screen_coords = []

        def interpolate(v0, v1, t):
            return v0 + t * (v1 - v0)

        for i in range(len(vertices)):
            v0, v1 = vertices[i], vertices[(i + 1) % len(vertices)]
            sv0, sv1 = screen_coords[i], screen_coords[(i + 1) % len(screen_coords)]

            if v0[2] >= near_plane:
                clipped_vertices.append(v0)
                clipped_screen_coords.append(sv0)

            if (v0[2] >= near_plane and v1[2] < near_plane) or (v0[2] < near_plane and v1[2] >= near_plane):
                t = (near_plane - v0[2]) / (v1[2] - v0[2])
                clip_vertex = [interpolate(v0[j], v1[j], t) for j in range(3)]
                clip_screen = [interpolate(sv0[j], sv1[j], t) for j in range(3)]
                clipped_vertices.append(clip_vertex)
                clipped_screen_coords.append(clip_screen)

        return clipped_vertices, clipped_screen_coords

def rotate2D(pos, rad):
    x, y = pos
    s, c = sin(rad), cos(rad)
    return x * c - y * s, y * c + x * s

def compute_normal(v0, v1, v2):
    u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    normal = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return normal

def get_bounding_box(vertices):
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    min_z = min(v[2] for v in vertices)
    max_z = max(v[2] for v in vertices)
    return (min_x, max_x, min_y, max_y, min_z, max_z)

def aabb_collision(box1, box2):
    min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = box1
    min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = box2
    
    return not (max_x1 < min_x2 or min_x1 > max_x2 or
                max_y1 < min_y2 or min_y1 > max_y2 or
                max_z1 < min_z2 or min_z1 > max_z2)

def point_in_triangle_2d(p, v0, v1, v2):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(p, v0, v1)
    d2 = sign(p, v1, v2)
    d3 = sign(p, v2, v0)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def point_in_triangle_3d(p, v0, v1, v2):
    bbox = get_bounding_box([v0, v1, v2])
    if not (bbox[0] <= p[0] <= bbox[1] and bbox[2] <= p[1] <= bbox[3] and bbox[4] <= p[2] <= bbox[5]):
        return False

    p2d = (p[0], p[1])
    v0_2d = (v0[0], v0[1])
    v1_2d = (v1[0], v1[1])
    v2_2d = (v2[0], v2[1])

    return point_in_triangle_2d(p2d, v0_2d, v1_2d, v2_2d)
