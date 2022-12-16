# This is the provided code for the ray tracing project.
#
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.

from __future__ import division
from util import *
import traceback

debug_flag = False   # print debug information when this is True
sphere_list = []     # holds sphere 
light_list = []
uvw_coords = []      #point on a surface object
#current_material = material() 



def setup():
    size(320, 320) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)
    frameRate(30)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# read and interpret a scene description .cli file based on which key has been pressed
def handleKeyPressed():
    if key == '1':
        interpreter("01_one_sphere.cli")
    elif key == '2':
        interpreter("02_three_spheres.cli")
    elif key == '3':
        interpreter("03_shiny_sphere.cli")
    elif key == '4':
        interpreter("04_many_spheres.cli")
    elif key == '5':
        interpreter("05_one_triangle.cli")
    elif key == '6':
        interpreter("06_icosahedron_and_sphere.cli")
    elif key == '7':
        interpreter("07_colorful_lights.cli")
    elif key == '8':
        interpreter("08_reflective_sphere.cli")
    elif key == '9':
        interpreter("09_mirror_spheres.cli")
    elif key == '0':
        interpreter("10_reflections_in_reflections.cli")

# You should add code for each command that calls routines that you write.
# Some of the commands will not be used until Part B of this project.
def interpreter(fname):
    global current_material, background_color, fov, eye_pos
    reset_scene()  # you should initialize any data structures that you will use here
    
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # parse the lines in the file in turn
    for line in lines:
        words = line.split()  # split up the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            radius = float(words[1])
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            center = PVector(x,y,z)
            # call your sphere making routine here
            # for example: create_sphere(x,y,z,radius)
            # create_sphere(center, radius)
            #sphere_list.append(create_sphere(center,radius))
            sphere_list.append(Sphere)
        elif words[0] == 'fov':
            fov = float(words[1])
            
        elif words[0] == 'eye':
            pass
        elif words[0] == 'uvw':
            pass
        elif words[0] == 'background':
            pass
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            pos = PVector(x,y,z)
            col = PVector(r,g,b) 
            light = lightClass(pos, col)
        elif words[0] == 'surface':
            #update surface
            #current_material(surface)
            pass
        elif words[0] == 'begin':
            pass
        elif words[0] == 'vertex':
            pass
        elif words[0] == 'end':
            pass
        elif words[0] == 'render':
            render_scene()    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

# render the ray tracing scene
def render_scene():
    global debug_flag
    print(fov)
    for j in range(height):
        for i in range(width):

            # Maybe set a debug flag to true for ONE pixel.
            # Have routines (like ray/sphere intersection)print extra information if this flag is set.
            debug_flag = False
            if i == 160 and j == 160:
                debug_flag = True

            # create an eye ray for pixel (i,j) and cast it into the scene
            pix_color = color(0.8, 0.2, 0.3)  # you will calculate the correct pixel color here using ray tracing
            set (i, j, pix_color)         # draw the pixel with the calculated color

# here you should reset any data structures that you will use for your scene (e.g. list of spheres)
def reset_scene():
    pass

# prints mouse location clicks, for help debugging
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

# this function should remain empty for this assignment
def draw():
    pass

#ray class. direction of ray and intersection?

#sphere. sphere is created by cli files. add to list of spheres. loop thru to see if they intersect 
#normal points out of center of sphere
class sphere():
    def create_sphere(center,radius): 
        self.center = center                        #try a grid data structure?
        self.radius = radius
        #current_material = diffuse
    
# (position, color)    
def lightClass(pos, col):
    pos = pos
    # lightColor = 
    #light contributes to hue. 
    #multiply color of object by color of light. rgb * rgb
    #strength of brightness is dot product of normal and light vector. normal that goes thru point p at center, ector of light frin kught source to point P. dont light after 90 degress (from dot product)
    #eye position is p vector    

#material class
# def material(position, color): 
