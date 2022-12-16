#helper functions file

#dot_product
#normalize 

#distance?
class helperFunctions(object):
    def __new__(cls, *args, **kwargs):
        print("numbah 1 baby")
        return super().__new__(cls)
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def distance(self, vert):
        return sqrt((vert.x - self.x) ** 2 + (vert.y - self.y) ** 2 + (vert.z - self.z) ** 2)
    
    def dot_product(self, a, b):
        # return (self.x * vector.x + self.y * vector.y + self.z + vector.z)
        return (a.x * b.x + a.y * b.y + a.z * b.z) 
   
    def normalizer(dir):  
        #get vector len
        x = dir[0]
        y = dir[1]
        z = dir[2]
        squared = x**2 + y**2 + z ** 2
        rooted = sqrt(squared)
        #normalize
        nX = x/rooted
        nY = y/rooted
        nZ = z/rooted
        direction = PVector(nX, nY, nZ)
        
#Ray class: stores origin and uvwection
class Ray:
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls)
    
    def __init__(self, origin, uvwection):
        self.origin = origin
        self.uvwection = uvwection   #direction

    def getLocation(self, t):
        global x, y, z
        x = self.origin.x + t * self.uvwection.x          #x(t) = Ox + t * dx
        y = self.origin.y + t * self.uvwection.y
        z = self.origin.z + t * self.uvwection.z
        vector = [x, y, z]
        return vector
        #return PVector(x,y,z)
        
class light_class:
    
    def __init__(self, pos, col):
        self.pos = pos
        self.col = col
    def new_light(pos, col):
        return
        
        
class sphere():
    def __new__(cls, *args, **kwargs):
        print("numbah 1 baby")
        return super().__new__(cls)
    
    def __init__(self, center,radius, surface_color): 
        self.center = center                        #try a grid data structure?
        self.radius = radius
        self.surface_color = surface_color

        
    #method to detect ray intersection with a given sphere
    def intersect(self, ray):
        global minT 
        minT = 1000
        #plug ray eq into implicit sphere
        #ray.uwection is nonetype, ray.origin is a pvector with no attribute 
        #a = ray.origin.dot_product(ray.uvwection) * minT**2
        a = dot_product(ray.uvwection, self.center) * minT**2
        b = dot_product((ray.origin -self.center), ray.uvwection) **2
        c = dot_product((ray.origin - self.center), (ray.origin - self.center)) - self.radius **2
        
        #B^2 - 4AC
        discriminant = (b*b - 4*a*c)
        minVal = 0
        if 0 < discriminant < minT: 
            results = [(-b+sqrt(discriminant))/(2*a), (-b-sqrt(discriminant))/(2*a)]
            minVal = min(results)
        return ray.getLocation(minVal)
            # store sphere info
            # set mint to sphere t value
