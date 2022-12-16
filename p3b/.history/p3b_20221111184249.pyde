# This is the provided code for the ray tracing project.
# Code by Alex Lindemann
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.

from __future__ import division
import traceback

debug_flag = False   # print debug information when this is True
sphere_list = []     # holds sphere 
candidates = []
light_list = []
vertices = []
norm_vector = []
global discriminant 
fov = 90 
x = 0
y = 0
z = 0
i = 0
j = 0


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
            sphere_list.append(sphere(center,radius, current_material))
        
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
            vertices = []
            
        elif words[0] == 'vertex':
            vertices.append(PVector(float(words[1]), float(words[2]), float(words[3])))
        elif words[0] == 'end':
            # sphere_list.append(triangle(vertices, diffuse[0], diffuse[1], diffuse[2], ambientRGB[0], ambientRGB[1], ambientRGB[2], 
            # specularRGB[0], specularRGB[1], specularRGB[2], specPower, kREFI))
            # sphere_list.append(triangle(vertices, diffuse.x, diffuse.y, diffuse.z, ambientRGB.x, ambientRGB.y, ambientRGB.z, 
            # specularRGB.x, specularRGB.y, specularRGB.z, specPower, kREFI))
            sphere_list.append(triangle(vertices, current_material))
            
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
    global i, j


    d = 1/(tan(radians(fov/2)))
    for j in range(height):
        #print("row", j)
        for i in range(width):
            U = (2*i)/width - 1
            V = (2*j)/height - 1 
            #V = V* -1
            uvwection = -d*uvw[2] + V*uvw[1] + U*uvw[0] 

            uvwection = uvwection.normalize()
            origin = eye          #Eye Position
            ray = Ray(origin, uvwection)
            candidates = []
            #get closest hit
            closest_hit = rayIntersect(ray)
            debug_flag = False
            if i == 160 and j == 160:
                debug_flag = True

            if len(closest_hit) == 0:
                pix_color = color(background_color.x, background_color.y, background_color.z)
                set(i,height-j, pix_color)
                #print(background_color)
            else:
                #print(candidates)
                # closestHit = min(candidates, key = lambda hit: hit.s.t)   
                pixColor = shade_function(closest_hit, ray, s)  
                #print(pixColor)
                pix_color = color(pixColor.x, pixColor.y, pixColor.z)
                set(i,height-j,pix_color)
                

            #*See if eye ray intersects with spheres


                    # Below doesn't work with triangles, but the other way fucks with the colors
                    # intersection_x = ray.origin.x + curr*ray.uvwection.x
                    # intersection_y = ray.origin.y + curr*ray.uvwection.y
                    # intersection_z = ray.origin.z + curr*ray.uvwection.z
                    # intersecption_point = PVector.add(ray.origin, PVector.dot(curr, ray.uvwection)) this isnt included idk what it is
                    # intersection_point = PVector(intersection_x, intersection_y, intersection_z)   
                    
                    #normalV = s.getNormal(intersection_point)
                    # normalV = PVector.normalize(intersection_point)
                    # curr_hit = direct_hit(s, normalV, curr, intersection_point) #curr = minT
                    # candidates.append(curr_hit)


                #----------


        
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

class triangle():
    
    def __init__(self, vert, surface_color):
        global vertices
        vertices = vert
        self.x, self.y, self.z = vertices
        self.yx = PVector.sub(self.y, self.x) #precompute sides of triangle
        self.zy = PVector.sub(self.z, self.y)
        self.xz = PVector.sub(self.x, self.z)
        self.surface_color = surface_color
        # self.dR = dr
        # self.dG = dg
        # self.dB = db
        # self.aR = ar
        # self.aG = ag
        # self.aB = ab
        # self.sR = sr
        # self.sG = sg
        # self.sB = sb
        # self.specPower = specPower
        # self.kREFI = kREFI
        self.normalized = PVector.cross(self.yx, PVector.mult(self.xz, -1)).normalize()

    def dot_product(a, b):
        return (a.x * b.x + a.y * b.y + a.z * b.z) 

    
    def intersect(self, ray):
        global debug_flag
        if i == 165 and j == 195:
            debug_flag = True 
        if debug_flag:
            print "testing intersection with triangle whose color is ", self.surface_color.diffuse
        #tri_intersect = self.normalized.dot_product(ray.uvwection)      #the ray equation * normal vector. (o + td - a) * N = 0
        tri_intersect = dot_product(self.normalized, ray.uvwection)
        self.x, self.y, self.z = vertices
        yx = PVector.sub(self.y, self.x) #precompute sides of triangle
        zy = PVector.sub(self.z, self.y)
        xz = PVector.sub(self.x, self.z)
        #dot of normal and ray direction, if negative flip ray direction
        norm_vector = PVector.cross(self.yx, xz).normalize()
        if PVector.dot(norm_vector, ray.uvwection) < 0:
            norm_vector = PVector.mult(norm_vector, -1)

        if tri_intersect == 0:
            return None
        t_value = float(PVector.dot(self.normalized, PVector.sub(self.x, ray.origin))) / tri_intersect   # t = N*(a-o)/(N*d)
        
        if debug_flag:
            print "xyz", self.x, self.y, self.z
            print "ray direction: ", ray.uvwection
            print "normal vector: ", self.normalized
            print "plane intersects at at t=%f" % t_value
        if t_value == 0:
           #ray is parallel to plane and never intersects 
            return None
        
        #find intersection
        #p is some that may or may not be on the plane. plug it into the ray equation P = o + td
        #point_P = ray.get_location(t_value)
        #t_d = PVector.dot(t_value, ray.uvwection)
        t_d = t_value * ray.uvwection
        point_P = PVector.add(ray.origin, t_d)

        p_vector = t_value
        

        #triples
        # aP = (point_P - self.x) #make sure its subtracting 
        aP = PVector.sub(point_P, self.x)
        bP = PVector.sub(point_P, self.y)
        cP = PVector.sub(point_P, self.z)
        # trip_X = (xy*aP).dot_product(normalized)
        someVar = PVector.cross(aP, yx) #this == (0.000000, 0.000000, -3.010363)
        trip_X = PVector.dot(norm_vector, PVector.cross(aP, yx)) #xy is a-b not b-a 
        trip_Y = PVector.dot(norm_vector, PVector.cross(bP, zy))
        trip_Z = PVector.dot(norm_vector, PVector.cross(cP, xz))

        if debug_flag:
            print "norm or xy*aP", aP  #norm_vector = (0.000000, -0.000000, -1.000000)
            print "triple 1: ", trip_X
            print "triple 2: ", trip_Y
            print "triple 3: ", trip_Z
    
        if trip_X > 0 and trip_Y > 0 and trip_Z > 0:
            #point is inside the triangle
            return point_P #return hit obj
        #also check if n * direction < 0 
        else:
            return None 
    

#sphere class. sphere is created by cli files. add to list of spheres. loop thru to see if they intersect 
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
        normalV = PVector.sub(intersection_point, self.center)
        normalV.normalize()
        return normalV
        

        #method to detect ray intersection with a given sphere

    
    def intersect(self, ray):
        minT = 1000000
        #plug ray eq into implicit sphere
        #ray.uwection is nonetype, ray.origin is a pvector with no attribute 
        uX = ray.origin.x - self.center.x
        uY = ray.origin.y - self.center.y
        uZ = ray.origin.z - self.center.z
        dX = ray.uvwection.x
        dY = ray.uvwection.y
        dZ = ray.uvwection.z
        a = (dX * dX) + (dY * dY) + (dZ * dZ)
        b = 2*dX*uX + 2*dY*uY + 2*dZ*uZ
        c = (uX*uX) + (uY*uY) + (uZ*uZ) - (self.radius**2)
        #a = dot_product(ray.uvwection*ray.uvwection, self.center*self.center) * minT**2
        #b = 2*(Dx*Ux) + 2*(Dy*Uy) + 2*Dz*Uz
        # b = dot_product((ray.origin -self.center), ray.uvwection) **2
        # c = dot_product((ray.origin - self.center), (ray.origin - self.center)) - self.radius **2
    
        
        #B^2 - 4AC
        discriminant = (b*b - 4*a*c)
        
        if 0 != discriminant: 
            candidates = [(-b+sqrt(discriminant))/(2*a), (-b-sqrt(discriminant))/(2*a)]
            closest_hit = min(candidates)
            if closest_hit != 0:
                int_pt = ray.get_location(closest_hit)
                normal_v = PVector.normalize(int_pt)
                return direct_hit(self, normal_v, closest_hit, int_pt) 
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

    def get_location(self, t):
        global x, y, z
        x = self.origin.x + t * self.uvwection.x          #x(t) = Ox + t * dx
        y = self.origin.y + t * self.uvwection.y
        z = self.origin.z + t * self.uvwection.z
        
        return PVector(x, y, z)

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
    
def shade_function(hit, ray, s): #need to pass in, p_vector,spec_power/current_material[~5], and ray?
    r_sum = 0
    g_sum = 0
    b_sum = 0
    # global light_list

    
    for light in light_list:
        L_vector = PVector.sub(light.pos, hit.intersection_point).normalize()
        #print("pos",light.pos)
        #print("ip", hit.intersection_point)
        c = max(dot_product(hit.n, L_vector), 0)
        r_sum += light.col.x * c * hit.s.surface_color.diffuse.x  #problem isnt these guys
        g_sum += light.col.y * c * hit.s.surface_color.diffuse.y
        b_sum += light.col.z * c * hit.s.surface_color.diffuse.z
        
         
        
        output = PVector(r_sum, g_sum, b_sum)        #pretty sure this is diffuse color
        #Specular Shading
        D = PVector.sub(ray.origin, hit.intersection_point).normalize()
        h_vector = PVector.sub(L_vector, D).normalize
        
        spec_coef = max(0, dot_product(L_vector, hit.n))**float(hit.s.surface_color.specPower)
        # someVar = PVector.pairwise_mult(light.col, hit.s.surface_color.)
        
        r_sum += hit.s.surface_color.specularRGB.x * light.col.x * spec_coef
        g_sum += hit.s.surface_color.specularRGB.y * light.col.y * spec_coef
        b_sum += hit.s.surface_color.specularRGB.z * light.col.z * spec_coef
        
        spec_col = PVector.mult((PVector.pairwise_mult(light.col, hit.s.surface_color.specularRGB)), spec_coef)
                    # pevector.mult spec_coef) 
    
        d_plus_s_col = PVector.add(output, spec_col) 
        # color_output = PVector.add(hit.s.surface_color.ambientRGB, d_plus_s_col)
        color_output = PVector(r_sum, g_sum, b_sum)
        
          #Shadows
        
        tiny_offset = PVector.mult(hit.n, 0.0001)
        s_origin = hit.intersection_point + tiny_offset
        s_direction = L_vector
        shadow_ray = Ray(s_origin, s_direction)
        global debug_flag

        if debug_flag:
            print "calculating contribution of the light whose position is: ", light.pos
            print "N: ", hit.n
            print "L: ", L_vector
            print "light color: ", light.col
            # print "surface's diffuse color: ", direct_hit.t_shape.mat.dif_color
    #end for loop
    
    #ambient 
    amb_col = hit.s.surface_color.ambientRGB
    true_color = PVector.add(amb_col, d_plus_s_col)
    
    
    
    if debug_flag:
        print("total color:", color_output)
    return color_output

#function
def rayIntersect(ray):
    minT = 1000
    closest_hit = None
    for s in sphere_list: 
        temp_hit = s.intersect(ray)
        # curr_hit = direct_hit(None, None, None, None)
        if temp_hit != None and temp_hit > 0 and temp_hit < minT:  #curr is a list
            # distance = calc_distance(curr, ray.origin) 
            minT = temp_hit.t
            closest_hit = temp_hit
            container = [minT, closest_hit]
            intersection_point = PVector.add(ray.origin, ray.uvwection)
            normalV = PVector.normalize(intersection_point)
            curr_hit = direct_hit(s, normalV, curr, intersection_point) #curr = minT
        return closest_hit
                 
class PVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "PVector(%f, %f, %f)" % (self.x, self.y, self.z)

    def __add__(self, other):
        return PVector.add(self, other)

    def __mul__(self, n):
        return PVector.mult(self, n)

    def __rmul__(self, n):
        return PVector.mult(self, n)

    def mag(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def magSq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def copy(self):
        return PVector(self.x, self.y, self.z)

    def div(self, n):
        return PVector(
            a.x / n,
            a.y / n,
            a.z / n,
        )

    @staticmethod
    def dist(a, b):
        return PVector.sub(a, b).mag()

    @staticmethod
    def add(a, b):
        return PVector(
            a.x + b.x,
            a.y + b.y,
            a.z + b.z,
        )

    @staticmethod
    def sub(a, b):
        return PVector(
            a.x - b.x,
            a.y - b.y,
            a.z - b.z,
        )

    @staticmethod
    def mult(a, n):
        return PVector(
            n * a.x,
            n * a.y,
            n * a.z,
        )

    @staticmethod
    def pairwise_mult(a, b):
        return PVector(
            a.x * b.x,
            a.y * b.y,
            a.z * b.z,
        )

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross(a, b):
        return PVector(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x,
        )

    def normalize(self):
        mag = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= mag
        self.y /= mag
        self.z /= mag
        return self
