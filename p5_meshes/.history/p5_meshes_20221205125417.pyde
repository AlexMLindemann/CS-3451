# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()
vTable = []
geoTable = []
opTable = {}
# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()
    

# draw the current mesh (you will modify parts of this routine)
def draw():
    
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix()

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
  
    beginShape()
    vertex (-1.0,  1.0, 0.0)
    vertex ( 1.0,  1.0, 0.0)
    vertex ( 0.0, -1.0, 0.0)
    endShape(CLOSE)
    
    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global vTable, geoTable, opTable
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        temp = []
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        temp.append(x)
        temp.append(y)
        temp.append(z)
        geoTable.append(temp)
        print "vertex: ", x, y, z
    



    # read in the faces (vTable)
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        vTable.append(index1)
        vTable.append(index2)
        vTable.append(index3)
        print "triangle: ", index1, index2, index3

    opTable = computeOTable(geoTable, vTable)
    #debugging 
    print_mesh()

#Compute opposite table
def computeOTable(geoTable, vTable):
    global opTable


    #bucket sort
    # compile list of triplets for each corner c
    triplets = []
    #c.next.vert
    for c in vTable:
        triplets.append([min(vTable[nextCorner(c)], vTable[prevCorner(c)]), max(vTable[nextCorner(c)], vTable[prevCorner(c)]), c])
        #triplets.append([min(nextCorner(c), prevCorner(c)), max(nextCorner(c), prevCorner(c)), c])
    print "next corner", geoTable[vTable[nextCorner(c)]]

    triplet_indices = {tuple(triplet): i for i, triplet in enumerate(triplets)}
    values = []
    for i in range(len(triplets)):
        values.append(i)
    # Sort the array of triplets
    sorted_triplets = sorted(triplets)
    mapped = zip(triplets, values)
    #print "mapped", set(mapped)
    print(mapped)

    print(triplets)
    # Iterate over the elements in the array
    # for i, triplet in enumerate(sorted_triplets):
    #     # Use the zip function to create pairs of triplets
    #     pairs = zip(sorted_triplets[i:], sorted_triplets[i + 1:])
    #     print "i, triplet loop"
    #     # Iterate over the pairs of triplets
    #     for pair in pairs:
    #         # Use the pairs as keys in the dictionary to fill out the opposite table entries
    #         cornerA = triplet_indices[tuple(pair[0])]
    #         cornerB = triplet_indices[tuple(pair[1])]
    #         opTable[cornerA] = cornerB
    # return opTable
    for i in range(0, len(sorted_triplets) - 1, 1):
        cornerA = sorted_triplets[i][2]
        print "cornerA: ", cornerA
        cornerB = sorted_triplets[i+1][2]
        print "cornerB: ", cornerB
        # opTable = {
        #     vTable[cornerA]: cornerB,
        #     vTable[cornerB]: cornerB
        #     }
        # print "opTable: " + str(opTable)

        opTable[sorted_triplets[i][2]] = vTable[sorted_triplets[i+1][2]]
        opTable[sorted_triplets[i+1][2]] = vTable[sorted_triplets[i][2]]
    return opTable 
 


# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    if key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == 'n': # next
        pass
    elif key == 'p': # previous
        pass
    elif key == 'o': # opposite
        pass
    elif key == 's': # swing
        pass
    elif key == 'd': # subdivide mesh
        print_mesh()
        #update global variables by calling subdivide 
        subdivideMesh()
    elif key == 'i': # inflate mesh
        pass
    elif key == 'r': # toggle random colors
        pass
    elif key == 'c': # toggle showing current corner
        pass
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY

#Helper Functions

def nextCorner(cornerNum):
    triNum = cornerNum // 3     
    nCorner = (3 * triNum + (cornerNum+1) % 3)
    return nCorner

def prevCorner(cornerNum):
    triNum = cornerNum // 3
    pCorner = (3 * triNum + (cornerNum-1) % 3)
    return pCorner

def oppositeCorner(cornerNum):
    # Use the opposite-table dictionary
    # Return O[cornerNum]
    return opTable[cornerNum]

#subdivision
def subdivideMesh(geoTable, vTable):
    global opTable
    opTable = computeOTable(geoTable, vTable)
    newVTable = []
    newGeoTable = geoTable
    print(newGeoTable)
    newGeoTable = []
    newGeoTable.copy(geoTable) 
    print(newGeoTable)
    print(geoTable)
    midpoints = {}
    for key, value in opTable.items(): #.items returns copy of dict list
        midpoint = key.prevCorner() + value.nextCorner()
        midIndex = len(newGeoTable)
        newGeoTable.append(midpoint)
        midpoints[key] = midIndex
        midpoints[value] = midIndex
    
    def subdivideMesh(vTable, geoTable, opTable):
        newOTable = opTable
        midpoints = {}
        newGTable = []
        newVTable = []
        numTris = len(vTable) // 2


        for a, b in newOTable:
            endPoint1 = geoTable[vTable[prevCorner(a)]]
            endPoint2 = geoTable[vTable[nextCorner(b)]]
            midpoint = PVector.mult(PVector.add(endPoint1, endPoint2), 0.5)
            midpointIndex = len(newGTable)
            newGTable.append(midpoint)
            midpoints[a] = midpointIndex
            midpoints[b] = midpointIndex

        for x in range(0, len(vTable), 3):
            y = x+1
            z = x+2
            newVTable.extend([(vTable[x], midpoints[z], midpoints[y]),
                          (midpoints[z], vTable[y], midpoints[x]),
                          (midpoints[y], midpoints[x], vTable[z]),
                          (midpoints[x], midpoints[z], midpoints[y])])
        return newVTable, newGTable, computeOTable(newGTable, newVTable)

def print_mesh():
    print "Vertex table (maps corner num to vertex num):"
    print "corner num\tvertex num:"
    for c, v in enumerate(vTable):
        print c, "\t\t", v
    print ""

    print "Opposite table (maps corner num to opposite corner num):"
    print "corner num\topposite corner num"
    for c, o in opTable.iteritems():
        print c, "\t\t", o
    print ""

    print "Geometry table (maps vertex num to position): "
    print "vertex num\tposition:"
    for v, g in enumerate(geoTable):
        print v, "\t\t", g
    print ""

    print ""
    print ""

class my_dictionary(dict):
 
  # __init__ function
  def __init__(self):
    self = dict()
 
  # Function to add key:value
  def add(self, key, value):
    self[key] = value

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

    def get(self):
        return PVector(self.x, self.y, self.z)

    def __getitem__(self, t):
        return getattr(self, ('x', 'y', 'z')[t])