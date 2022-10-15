from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 512
height = 512

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (1,1,1), spec = 8)

face = Material(diffuse = (2.10, 1.61, 1.40), spec = 8)
shirt = Material(diffuse = (0, 1.61, 0), spec = 8)
lips=Material(diffuse = (5, 0, 0), spec = 8)
eyes=Material(diffuse=(2, 1, 1),spec = 64, texture = Texture("marble.bmp"), matType= REFLECTIVE)
pupil=Material(diffuse = (0.5, 0.5, 0.5), spec = 8)
hair =Material(diffuse = (1.5, 0.75, 0), spec = 8)

door=Material(diffuse = (2.55, 2.55, 0), spec = 8)

marble = Material(spec = 64, texture = Texture("marble.bmp"), matType= REFLECTIVE)
wall = Material(spec = 80, texture = Texture("wall.bmp"), matType= REFLECTIVE)

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType = TRANSPARENT)

rtx = Raytracer(width, height)

rtx.envMap = Texture("parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
# rtx.lights.append( DirectionalLight(direction = (0,0,-1), intensity = 0.5 ))
rtx.lights.append( PointLight(point = (-3,1,5), color=(0.5,0.5,0.5) ))
rtx.lights.append( PointLight(point = (0,1,-10), color=(0.5,0.5,0.5) ))


rtx.scene.append( Plane(position = (0,-10,0), normal = (0,1,0), material = stone ))
# rtx.scene.append( Plane(position = (0,10,0), normal = (0,-1,0), material = stone ))
# rtx.scene.append( Plane(position = (-10,0,0), normal = (1,0,0), material = stone ))
# rtx.scene.append( Plane(position = (10,0,0), normal = (-1,0,0), material = stone ))
# rtx.scene.append( Plane(position = (0,0,-40), normal = (0,0,1), material = stone ))

# face
rtx.scene.append( Sphere(V3(-1,0,-3), 0.5, face)  )
# Nose
rtx.scene.append( Sphere(V3(-0.9,-0.06,-2.5), 0.1, face)  )

# eyebrow, eye and pupil
# rtx.scene.append( Disk(position = (-1.1,0.24,-2.5), radius = 0.1, normal = (0,1,0), material = hair ))
# rtx.scene.append( Sphere(V3(-1.09,0.1,-2.5), 0.1, eyes)  )
# rtx.scene.append( Sphere(V3(-1.06,0.1,-2.4), 0.06, pupil)  )

# eyebrow, eye and pupil
rtx.scene.append( Disk(position = (-0.6,0.24,-2.5), radius = 0.1, normal = (0,1,0), material = hair ))
rtx.scene.append( Sphere(V3(-0.6,0.1,-2.5), 0.1, eyes)  )
rtx.scene.append( Sphere(V3(-0.56,0.1,-2.3), 0.06, pupil)  )

# hair
rtx.scene.append( Disk(position = (-0.9,0.6,-2.7), radius = 0.2, normal = (0.1,0,0), material = hair ))

# mouth
rtx.scene.append( Disk(position = (-0.8,-0.2,-2.3), radius = 0.2, normal = (0,1,0), material = lips ))

# shirt
rtx.scene.append( Sphere(V3(-1,-1,-3), 0.5, shirt)  )
# rtx.scene.append( Sphere(V3(-1,-1.3,-3), 0.5, shirt)  )
# rtx.scene.append( Sphere(V3(-1,-1.6,-3), 0.5, shirt)  )

# doors
rtx.scene.append( AABB(position = (-1,-4,-18), size = (2,2,2), material = door))
# rtx.scene.append( AABB(position = (-1,-2,-18), size = (2,2,2), material = door))
# rtx.scene.append( AABB(position = (1,-4,-18), size = (2,2,2), material = door))
# rtx.scene.append( AABB(position = (1,-2,-18), size = (2,2,2), material = door))
# rtx.scene.append( AABB(position = (1,-1,-18), size = (2,2,2), material = door))
# rtx.scene.append( AABB(position = (-1,-1,-18), size = (2,2,2), material = door))


rtx.glRender()

rtx.glFinish("output.bmp")