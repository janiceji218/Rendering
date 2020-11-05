from utils import *
from ray import *
from cli import render

tan = Material(vec([0.4, 0.4, 0.2]), k_s=0.3, p=90, k_m=0.3)
blue = Material(vec([0.2, 0.2, 0.5]), k_m=0.5)
gray = Material(vec([0.2, 0.2, 0.2]), k_m=0.4)
white = Material(vec([1.0, 1.0, 1.0]), k_m=0.4)
black = Material(vec([0.0, 0.0, 0.0]), k_m=0.0)
orange = Material(vec([0.8, 0.393, 0.0]), k_m=0.0)
red = Material(vec([1.0, 0.05, 0.05]), k_m=0.2)

scene = Scene([
    Sphere(vec([0,-1,0]), 0.45, white),
    Sphere(vec([0,-0.32,0]), 0.35, white),
    Sphere(vec([0, 0.2, 0]), 0.26, white),
    Sphere(vec([0, 0.4, 0]), 0.2, red),
    Sphere(vec([0.2,0.2,0.2]), 0.05, orange), #nose
    Sphere(vec([0.06,0.27,0.28]), 0.042, black), #left eye
    Sphere(vec([0.25,0.27,0.1]), 0.042, black), #right eye
    Sphere(vec([0,-41,0]), 39.7, white),
])

lights = [
    PointLight(vec([12,10,5]), vec([300,300,300])),
    AmbientLight(0.1),
]

camera = Camera(vec([3,1,5]), target=vec([0,-0.4,0]), vfov=24, aspect=16/9)

render(camera, scene, lights)