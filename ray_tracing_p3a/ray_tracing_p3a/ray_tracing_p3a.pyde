# This is the provided code for the ray tracing project.
# Code by Alex Lindemann
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.

from __future__ import division
import helperFunctions 
import traceback

debug_flag = False   # print debug information when this is True
sphere_list = []     # holds sphere 
candidates = []
light_list = []
norm_vector = []
global discriminant 
fov = 90 
x = 0
y = 0
z = 0

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
            sphere_list.append(sphere(center,radius, diffuse))
        
        elif words[0] == 'fov':
            global fov
            fov = float(words[1])
            
        elif words[0] == 'eye':
            global eye
            eye = PVector(float(words[1]), float(words[2]), float(words[3]))
            
        elif words[0] == 'uvw':
            global uvw
            # if (float(words[1])) == 1:                
                # x = float(words[1])
            x = PVector(float(words[1]), float(words[2]), float(words[3]))
            y = PVector(float(words[4]), float(words[5]), float(words[6]))
            z = PVector(float(words[7]), float(words[8]), float(words[9]))
            uvw = [x, y, z]
            # else:
            #     z = PVector(words[1], words[2], words[3])
            #     y = PVector(words[4], words[5], words[6])
            #     x = PVector(words[7], words[8], words[9])
            #     uvw = [x, y, z]

        elif words[0] == 'background':
            r = float(words[1])
            g = float(words[2])
            b = float(words[3])
            background_color = PVector(r,g,b)
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            pos = PVector(x,y,z)
            col = PVector(r,g,b) 
            light = light_class(pos, col)
            light_list.append(light)
            
        elif words[0] == 'surface':
            diffuse = PVector(float(words[1]), float(words[2]), float(words[3]))
            ambientRGB = PVector(float(words[4]), float(words[5]), float(words[6]))
            specularRGB = PVector(float(words[7]), float(words[8]), float(words[9]))
            specPower = words[10]
            kREFI = words[11]
            current_material = material(diffuse, ambientRGB, specularRGB, specPower, kREFI)
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
    global light_list
    global eye

    print "shapes:"
    for shape in sphere_list:
        print shape.radius, shape.center, shape.surface_color
    print "lights:"
    for light in light_list:
        print light.pos, light.col
    print "eye position: ", eye
    print "uvw", uvw
    print "fov", fov
    print "bg_color", background_color    

    d = 1/(tan(radians(fov/2)))
    for j in range(height):
        print("row", j)
        for i in range(width):
            U = (2*i)/width - 1
            V = (2*j)/height - 1 
            #V = V* -1
            uvwection = -d*uvw[2] + V*uvw[1] + U*uvw[0] 
            #uvwection = PVector(U, V, -1)   
  
            #uvwection = normalizer(uvwection)
            uvwection = uvwection.normalize()
            origin = eye          #Eye Position
            ray = Ray(origin, uvwection)
            candidates = []
            debug_flag = False
            if i == 160 and j == 160:
                debug_flag = True

            #*See if eye ray intersects with spheres
            minT = 10000
            for s in sphere_list: 
                curr = s.intersect(ray)
                # curr_hit = direct_hit(None, None, None, None)
                if curr != None:  #curr is a list
                    # distance = calc_distance(curr, ray.origin) 
                    #minT is a list????
                    intersection_x = ray.origin.x + curr*(ray.uvwection.x)
                    intersection_y = ray.origin.y + curr*ray.uvwection.y
                    intersection_z = ray.origin.z + curr*ray.uvwection.z
                    intersection_point = PVector(intersection_x, intersection_y, intersection_z)   
                    normalV = s.getNormal(intersection_point)
                    curr_hit = direct_hit(s, normalV, curr, intersection_point) #curr = minT
                    candidates.append(curr_hit)
                 

                #----------
        
            if len(candidates) == 0:
                pix_color = color(background_color.x, background_color.y, background_color.z)
                set(i,height-j, pix_color)
                #print(background_color)
            else:
                #print(candidates)
                closestHit = min(candidates, key = lambda hit: hit.t)   
                pixColor = shade_function(closestHit)  
                #print(pixColor)
                pix_color = color(*pixColor)
                set(i,height-j,pix_color)
        
            # print(pix_color)
            # Maybe set a debug flag to true for ONE pixel.
            # Have routines (like ray/sphere intersection)print extra information if this flag is set.

            
            # create an eye ray for pixel (i,j) and cast it into the scene
            # pix_color = color(0.8, 0.2, 0.3)  # you will calculate the correct pixel color here using ray tracing
            # set (i, j, pix_color)         # draw the pixel with the calculated color

#try using the py normalize fn
def normalizer(uvw):
    #get vector len
    x = uvw[0]
    y = uvw[1]
    z = uvw[2]
    squared = x**2 + y**2 + z ** 2
    rooted = sqrt(squared)
    #normalize
    nX = x/rooted
    nY = y/rooted
    nZ = z/rooted
    uvwection = PVector(nX, nY, nZ)
    #uvwection = [nX, nY, nZ]
    return uvwection
# here you should reset any data structures that you will use for your scene (e.g. list of spheres)
def reset_scene():
    global sphere_list
    global candidates
    global light_list
    global x, y, z
    sphere_list = []     # holds sphere 
    candidates = []
    light_list = []
    x = 0
    y = 0
    z = 0
    global discriminant 
    discriminant = 0
    global fov
    fov = 0
    

    

# prints mouse location clicks, for help debugging
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

# this function should remain empty for this assignment
def draw():
    pass

#ray class. uvwection of ray and intersection?

#sphere. sphere is created by cli files. add to list of spheres. loop thru to see if they intersect 
#normal points out of center of sphere
class sphere():
    def __new__(cls, *args, **kwargs):
        print("numbah 1 baby")
        return super().__new__(cls)
    
    def __init__(self, center,radius, surface_color): 
        self.center = center                        #try a grid data structure?
        self.radius = radius
        self.surface_color = surface_color

        
    def getNormal(self, intersection_point):
        normalV = intersection_point - self.center
        normalV.normalize()
        return normalV
        

        #method to detect ray intersection with a given sphere

    
    def intersect(self, ray):
        minT = 1000000
        #plug ray eq into implicit sphere
        #ray.uwection is nonetype, ray.origin is a pvector with no attribute 
        uX = ray.origin[0] - self.center[0]
        uY = ray.origin[1] - self.center[1]
        uZ = ray.origin[2] - self.center[2]
        dX = ray.uvwection[0]
        dY = ray.uvwection[1]
        dZ = ray.uvwection[2]
        a = (dX * dX) + (dY * dY) + (dZ * dZ)
        b = 2*dX*uX + 2*dY*uY + 2*dZ*uZ
        c = (uX*uX) + (uY*uY) + (uZ*uZ) - (self.radius**2)
        #a = dot_product(ray.uvwection*ray.uvwection, self.center*self.center) * minT**2
        #b = 2*(Dx*Ux) + 2*(Dy*Uy) + 2*Dz*Uz
        # b = dot_product((ray.origin -self.center), ray.uvwection) **2
        # c = dot_product((ray.origin - self.center), (ray.origin - self.center)) - self.radius **2
        if debug_flag:
            print "testing intersection with the sphere whose color is ", self.surface_color # change these variable names to match the rest of your code!
            print "a, b, c coefficients of the quadratic: ", a, b, c
        
        #B^2 - 4AC
        discriminant = (b*b - 4*a*c)
        if 0 < discriminant: 
            minT = (-b-sqrt(discriminant))/(2*a)
            return minT
            #return ray.getLocation(minT)
        else: 
            return None
            # store sphere info
            # set mint to sphere t value
        

def dot_product(a, b):
    # return (self.x * vector.x + self.y * vector.y + self.z + vector.z)
    return (a.x * b.x + a.y * b.y + a.z * b.z) 
   
#hit class

class direct_hit:
    def __init__(self, s, n, t, intersection_point):
        self.s = s
        self.n = n
        self.t = t
        self.intersection_point = intersection_point

    
                   
#Ray class: stores origin and uvwection
class Ray:
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls)
    
    def __init__(self, origin, uvwection):
        self.origin = origin
        self.uvwection = uvwection   #direction

    # def getLocation(self, t):
    #     global x, y, z
    #     x = self.origin.x + t * self.uvwection.x          #x(t) = Ox + t * dx
    #     y = self.origin.y + t * self.uvwection.y
    #     z = self.origin.z + t * self.uvwection.z
    #     vector = [x, y, z]
    #     return vector
        #return PVector(x,y,z)

class light_class:
    
    def __init__(self, pos, col):
        self.pos = pos
        self.col = col
    def new_light(pos, col):
        return
        
            

#material class
class material:
    def __new__(cls, *args, **kwargs):
        print("numbah 1 baby")
        return super()._new_(cls)
    def __init__(self, diffuse, ambientRGB, specularRGB, specPower, kREFI): 
        self.diffuse = diffuse
        self.ambientRGB = ambientRGB
        self.specularRGB = specularRGB
        self.specPower = specPower
        self.kREFI = kREFI
    
def shade_function(hit):
    r_sum = 0
    g_sum = 0
    b_sum = 0
    # global light_list
    
    for light in light_list:
        L_vector = (light.pos - hit.intersection_point).normalize()
        #print("pos",light.pos)
        #print("ip", hit.intersection_point)
        c = max(dot_product(hit.n, L_vector), 0)
        r_sum += light.col.x * c * hit.s.surface_color.x
        g_sum += light.col.y * c * hit.s.surface_color.y
        b_sum += light.col.z * c * hit.s.surface_color.z
        if debug_flag:
            print "calculating contribution of the light whose position is: ", light.pos
            print "N: ", hit.n
            print "L: ", L_vector
            print "light color: ", light.col
            # print "surface's diffuse color: ", direct_hit.t_shape.mat.dif_color
    output = (r_sum, g_sum, b_sum)
    
    if debug_flag:
        print("total color:", output)
    return output
