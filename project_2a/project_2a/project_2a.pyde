# Object Modeling Example Code

from __future__ import division
import traceback

time = 0   # time is used to move objects from one frame to another

def setup():
    size (800, 800, P3D)
    try:
        frameRate(120)       # this seems to be needed to make sure the scene draws properly
        perspective (60 * PI / 180, 1, 0.1, 1000)  # 60-degree field of view
    except Exception:
        traceback.print_exc()

def draw():
    try:
        global time
        time += 0.01

        camera (0, 0, 100, 0, 0, 0, 0,  1, 0)  # position of the virtual camera

        background (200, 200, 255)  # clear screen and set background to light blue
        
        # set up the lights
        ambientLight(50, 50, 50);
        lightSpecular(255, 255, 255)
        directionalLight (100, 100, 100, -0.3, 0.5, -1)
        
        # set some of the surface properties
        noStroke()
        specular (180, 180, 180)
        shininess (1.0)
#========BelowTheBelt==================================================
        # leg left
        fill (255, 0, 0)
        pushMatrix()
        rotateY(-time)
        translate (-4, 18, 0)
        rotateX(PI/2.0)
        #rotateX (time)
        scale(5,3,10)
        cylinder()
        popMatrix()
        
        # leg right
        fill (255, 0, 0)
        pushMatrix()
        rotateY(-time)
        translate (4, 18, 0)
        rotateX(PI/2.0)     #use of rotate in building the object
        #rotateX (time)
        scale(5,3,10)
        cylinder()
        popMatrix()
        
        #foot 1
        fill(155, 211, 221)
        pushMatrix()
        rotateY(-time)
        translate(4, 30, 0)
        sphereDetail(30)
        scale(0.75, 0.5)
        sphere(5)
        popMatrix()
        #foot 2
        fill(155, 211, 221)
        pushMatrix()
        rotateY(-time)
        translate(-4, 30, 0)
        sphereDetail(30)
        scale(0.75, 0.5)
        sphere(5)
        popMatrix()
#=================================================================
        # stewie's head 
        fill (233, 208, 160)
        pushMatrix()
        #translate (0, 8 * sin(4 * time), 0)  # move up and down
        translate(0, -15, 0)
        rotateY(-time*5)
        sphereDetail(60)  # this controls how many polygons make up each sphere
        scale(2.0, 1.25)
        sphere(10)
        popMatrix()

        #left eye
        fill(0, 0, 0)
        pushMatrix()
        rotateY(-time*5)
        translate(-8,-15,9.5)
        torus(2, 0.5, 16, 16)
        popMatrix()
        
        #right eye
        fill (0,0,0)
        pushMatrix()
        
        rotateY(-time*5)
        
        translate(8, -15, 9.5)
        torus(2, 0.5, 16, 16)
        popMatrix()
        
        #eyebrow left
        fill(1,1,1)
        pushMatrix()
        # rotateY(-PI/5)
        rotateY(-time*5)
        translate (-8, -20, 8.5)
        box(4, 0.5, 0.5)
        popMatrix() 
        
        #eyebrow right #9 
        fill(0,0,0)
        pushMatrix()
        rotateY(-time*5)
        translate (8, -20, 8.5)
        box(4, 0.5, 0.5)
        popMatrix() 
        
        #nose
        fill(1, 1, 1)
        pushMatrix()
        rotateY(-time*5)
        translate(0,-13,10)
        #rotateZ(PI/3)
        cone(5)
        popMatrix()
        
#===========================
        #torso
        fill(255,0,0)
        pushMatrix()
        rotateY(-time)
        translate (0, 1, 0)
        box(20, 15, 10)
        popMatrix()
       
         #left arm 12
        fill(255,233,0)
        pushMatrix()
        rotateY(-time)
        translate(-12, 4, 0)
        box(4, 20, 8)
        popMatrix()
        
        #right arm
        fill(255,233,0)
        pushMatrix()
        rotateY(-time)
        translate(12, 4, 0)
        box(4, 20, 8)
        popMatrix()
        
        
    except Exception:
        traceback.print_exc()

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 50):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # round main body
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2
# Draw a cone pointing in the -y direction (up), with radius 1, with y in range [-1, 1]
def cone(sides=50):
    sides = int(sides)

    # draw triangles making up the sides of the cone
    for i in range(sides):
        theta = 2.0 * PI * i / sides
        theta_next = 2.0 * PI * (i + 1) / sides
        
        beginShape()
        normal(cos(theta), 0.6, sin(theta))
        vertex(cos(theta), 1.0, sin(theta))
        normal(cos(theta_next), 0.6, sin(theta_next))
        vertex(cos(theta_next), 1.0, sin(theta_next))
        normal(0.0, -1.0, 0.0)
        vertex(0.0, -1.0, 0.0)
        endShape()

    # draw the cap of the cone
    beginShape()
    for i in range(sides):
        theta = 2.0 * PI * i / sides
        vertex(cos(theta), 1.0, sin(theta))
    endShape()
    
# Draw a torus flat in the XY plane
def torus(radius=1.0, tube_radius=0.5, detail_x=16, detail_y=16):
    radius = float(radius)
    tube_radius = float(tube_radius)
    detail_x = int(detail_x)
    detail_y = int(detail_y)

    tube_ratio = (tube_radius / radius)

    def make_torus():
        vertices = []
        normals = []
        for torus_segment in range(detail_x):
            theta = 2 * PI * torus_segment / detail_x
            cos_theta = cos(theta)
            sin_theta = sin(theta)

            segment_vertices = []
            segment_normals = []

            for tube_segment in range(detail_y):
                phi = 2 * PI * tube_segment / detail_y
                cos_phi = cos(phi)
                sin_phi = sin(phi)
                segment_vertices.append(PVector(
                    cos_theta * (radius + cos_phi * tube_radius),
                    sin_theta * (radius + cos_phi * tube_radius),
                    sin_phi * tube_radius,
                ))
                segment_normals.append(PVector(
                    cos_phi * cos_theta,
                    cos_phi * sin_theta,
                    sin_phi,
                ))
            vertices.append(segment_vertices)
            normals.append(segment_normals)
        return vertices, normals

    global GEOMETRY_CACHE
    try:
        GEOMETRY_CACHE
    except NameError:
        GEOMETRY_CACHE = {}
    cache_index = ("torus", radius, tube_radius, detail_x, detail_y)
    if cache_index in GEOMETRY_CACHE:
        vertices, normals = GEOMETRY_CACHE[cache_index]

    else:
        vertices, normals = make_torus()
        GEOMETRY_CACHE[cache_index] = (vertices, normals)

    for i in range(detail_x):
        for j in range(detail_y):
            beginShape()

            normal(normals[i][j].x, normals[i][j].y, normals[i][j].z)
            vertex(vertices[i][j].x, vertices[i][j].y, vertices[i][j].z)
            normal(normals[(i + 1) % detail_x][j].x, normals[(i + 1) % detail_x][j].y, normals[(i + 1) % detail_x][j].z)
            vertex(vertices[(i + 1) % detail_x][j].x, vertices[(i + 1) % detail_x][j].y, vertices[(i + 1) % detail_x][j].z)
            normal(normals[(i + 1) % detail_x][(j + 1) % detail_y].x, normals[(i + 1) % detail_x][(j + 1) % detail_y].y, normals[(i + 1) % detail_x][(j + 1) % detail_y].z)
            vertex(vertices[(i + 1) % detail_x][(j + 1) % detail_y].x, vertices[(i + 1) % detail_x][(j + 1) % detail_y].y, vertices[(i + 1) % detail_x][(j + 1) % detail_y].z)
            normal(normals[i][(j + 1) % detail_y].x, normals[i][(j + 1) % detail_y].y, normals[i][(j + 1) % detail_y].z)
            vertex(vertices[i][(j + 1) % detail_y].x, vertices[i][(j + 1) % detail_y].y, vertices[i][(j + 1) % detail_y].z)

            endShape(CLOSE)
