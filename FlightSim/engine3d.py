# engine3d.py
# A small 3D renderer for Thumby, adapted from TinyCircuits' "Foxgine" tech demo
# (TinyCircuits-Thumby-Games/Foxgine). Reworked for FlightSim:
#   - precomputes sin/cos once per frame instead of once per vertex (Foxgine
#     called rotate2D, and therefore sin/cos, for every single vertex)
#   - fixes a backface-culling bug where the depth/bounds check indexed
#     vert_list[i] (the loop counter) instead of vert_list[face[i]]
#   - supports arbitrary N-gon faces instead of a hardcoded tri/quad split
#   - adds an optional screen-space "roll" term so the camera can bank,
#     which the original engine had no concept of
#   - adds a simple near-plane clip (skip a face if any vertex is behind
#     the camera) so the plane can pass close to geometry without the
#     perspective divide blowing up

from math import sin, cos

class Model:
    # verts: list of (x, y, z) tuples, object-space
    # faces: list of (indices, color, cull) where indices is a tuple/list
    #        of >=3 vertex indices (drawn as a fan for filled/backface use),
    #        color is 0-3 (thumbyGrayscale colour), cull is 1 to enable
    #        backface culling or 0 to always draw both sides
    __slots__ = ("verts", "faces")
    def __init__(self, verts, faces):
        self.verts = verts
        self.faces = faces


class Entity:
    # A placed instance of a Model. pos is world-space (x, y, z).
    # wire=True forces wireframe (edges only) regardless of the global
    # render mode - used for checkpoint gates.
    __slots__ = ("model", "pos", "wire")
    def __init__(self, model, pos, wire=False):
        self.model = model
        self.pos = pos
        self.wire = wire


def _dist2(pos, cam_pos):
    dx = pos[0] - cam_pos[0]
    dy = pos[1] - cam_pos[1]
    dz = pos[2] - cam_pos[2]
    return dx * dx + dy * dy + dz * dz


def _clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


class Renderer:
    def __init__(self, display, screen_w, screen_h, fov=60, near=0.2):
        self.display = display
        self.w = screen_w
        self.h = screen_h
        self.cx = screen_w // 2
        self.cy = screen_h // 2
        self.fov = fov
        self.near = near
        self.fill_mode = True  # True = filled polygons, False = wireframe

    def draw(self, entities, cam_pos, yaw, pitch, roll):
        sy, cy_ = sin(yaw), cos(yaw)
        sp, cp = sin(pitch), cos(pitch)
        sr, cr = sin(roll), cos(roll)
        fov = self.fov
        near = self.near
        cx, cy = self.cx, self.cy
        camx, camy, camz = cam_pos

        # painter's algorithm: draw far entities first
        ordered = sorted(entities, key=lambda e: _dist2(e.pos, cam_pos), reverse=True)

        for ent in ordered:
            model = ent.model
            ex, ey, ez = ent.pos
            ox = ex - camx
            oy = ey - camy
            oz = ez - camz

            cam_space = []   # camera-space (x, y, z) per vertex
            screen = []      # (sx, sy) per vertex
            for (vx, vy, vz) in model.verts:
                wx = vx + ox
                wy = vy + oy
                wz = vz + oz

                # yaw (rotate x/z around the vertical axis)
                x1 = wx * cy_ - wz * sy
                z1 = wz * cy_ + wx * sy
                # pitch (rotate y/z)
                y1 = wy * cp - z1 * sp
                z2 = z1 * cp + wy * sp

                cam_space.append((x1, y1, z2))

                if z2 > near:
                    f = fov / z2
                    dx = x1 * f
                    dy = y1 * f
                    if roll:
                        dxr = dx * cr - dy * sr
                        dyr = dx * sr + dy * cr
                        dx, dy = dxr, dyr
                    sx = cx + int(_clamp(dx, -2000, 2000))
                    sy_ = cy - int(_clamp(dy, -2000, 2000))
                    screen.append((sx, sy_))
                else:
                    screen.append(None)

            for face in model.faces:
                indices, color, cull = face

                # near-plane clip: skip faces with any vertex behind camera
                skip = False
                for i in indices:
                    if screen[i] is None:
                        skip = True
                        break
                if skip:
                    continue

                if cull:
                    v0 = cam_space[indices[0]]
                    v1 = cam_space[indices[1]]
                    v2 = cam_space[indices[2]]
                    ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
                    vx_, vy_, vz_ = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
                    nz = ux * vy_ - uy * vx_
                    if nz >= 0:
                        continue

                pts = [screen[i] for i in indices]

                if ent.wire or not self.fill_mode:
                    self._draw_edges(pts, color)
                else:
                    self._fill_poly(pts, color)

    def _draw_edges(self, pts, color):
        n = len(pts)
        draw_line = self.display.drawLine
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            draw_line(x0, y0, x1, y1, color)

    def _fill_poly(self, pts, color):
        display = self.display
        n = len(pts)
        min_y = pts[0][1]
        max_y = pts[0][1]
        for p in pts:
            if p[1] < min_y:
                min_y = p[1]
            if p[1] > max_y:
                max_y = p[1]
        min_y = max(min_y, 0)
        max_y = min(max_y, self.h - 1)
        if min_y > max_y:
            return

        set_pixel = display.setPixel
        for y in range(min_y, max_y + 1):
            xs = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if len(xs) < 2:
                continue
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                xa = max(int(xs[j]), 0)
                xb = min(int(xs[j + 1]), self.w - 1)
                for x in range(xa, xb + 1):
                    set_pixel(x, y, color)
