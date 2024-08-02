import thumbyButton as buttons
from math import sin, cos, radians
import ujson
from sys import path as syspath
syspath.insert(0, '/Games/Foxgine')
from thumbyGrayscale import display
from Cam import Cam
from Obj3D import Object3D

w, h = 72, 40
cx, cy = w // 2, h // 2
fov = 50
dt = 1 / 30
rendType = 0
gameStart = 0
rendAmt = 2
objects = []
objPositions = [[0,0,0]]

display.setFont("/lib/font3x5.bin", 3, 5, 1)
display.setFPS(30)

cam = Cam((0, 1, -5))
file_path = "/Games/Foxgine/models.txt"

try:
    with open(file_path, "r") as file:
        fileObjs = ujson.load(file)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    fileObjs = {}

def makeObjs(fileObjs, rendType):
    objMaker = []
    objPos = [[0, 0, 0], [0, 0, 5], [0, 1, 0]]
    combinedObjs = ["quad", "tri", "test"]
    
    combined_verts = []
    combined_polys = []
    
    vert_offset = 0

    for i, obj_name in enumerate(combinedObjs):
        verts = fileObjs[obj_name]["Verticies"]
        polys = fileObjs[obj_name]["Polygons"]
        pos = objPos[i]
        
        for vert in verts:
            combined_verts.append([vert[0] + pos[0], vert[1] + pos[1], vert[2] + pos[2]])
        
        for poly in polys:
            adjusted_poly = [index + vert_offset if isinstance(index, int) else index for index in poly]
            combined_polys.append(adjusted_poly)
        
        vert_offset += len(verts)
    
    fileObjs["combined"]["Verticies"] = combined_verts
    fileObjs["combined"]["Polygons"] = combined_polys
    
    print(fileObjs["combined"]["Verticies"])
    print(fileObjs["combined"]["Polygons"])

    objMaker.append(Object3D(fileObjs, "combined", (0, 0, 0), rendType))
    objMaker.append(Object3D(fileObjs, "tris", (1.5, 0, 0), rendType))
    
    for obj_name in combinedObjs:
        fileObjs[obj_name]["Verticies"].clear()
        fileObjs[obj_name]["Polygons"].clear()
    
    objPos.clear()
    combinedObjs.clear()
    
    return objMaker

def distance(obj, cam):
    dx = obj.pos[0] - cam.pos[0]
    dy = obj.pos[1] - cam.pos[1]
    dz = obj.pos[2] - cam.pos[2]
    return dx * dx + dy * dy + dz * dz

while True:
    display.update()
    display.fill(0)

    if gameStart == 1:
        objects.sort(key=lambda obj: distance(obj, cam), reverse=True)
        for obj in objects:
            obj.render(fov, (w, h), (cx, cy), cam, -1, 20)
        
        cam.update(dt, buttons, objects)

        display.drawText("X: " + str(int(cam.pos[0])), 2, 2, 2)
        display.drawText("Y: " + str(int(cam.pos[1])), 2, 8, 2)
        display.drawText("Z: " + str(int(cam.pos[2])), 35, 8, 2)
        display.drawText("Style: " + str(cam.style), 35, 2, 2)
    elif gameStart == 0:
        display.drawText("Press A for...", 10, 3, 1)
        display.drawText("Filled Polys!", 10, 10, 2)

        display.drawText("Press B for...", 10, 26, 1)
        display.drawText("Lined Polys!", 10, 33, 2)

        if buttons.buttonA.justPressed():
            rendType = 1
            gameStart = 1
            objects = makeObjs(fileObjs, rendType)
        if buttons.buttonB.justPressed():
            rendType = 0
            gameStart = 1
            objects = makeObjs(fileObjs, rendType)