# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback
import random

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()
vTable = []
geoTable = []
opTable = {}
colFlag = False
currC = 0
currCVisible = False
# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()
    

# draw the current mesh (you will modify parts of this routine)
def draw():
    background (100, 100, 180)    # clear the screen to black
    randomSeed(0)
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
    # beginShape()
    # vertex (-1.0,  1.0, 0.0)
    # vertex ( 1.0,  1.0, 0.0)
    # vertex ( 0.0, -1.0, 0.0)
    # endShape(CLOSE)
    
    #. Iterate starting from 0 to len(V-table), adding 3 to the iterator each time (eg 0, 3, 6, ...)Let iterator variable be c
    for c in range(-1, len(vTable), 3):
        beginShape()
        print "we're in the table" 
        print "len vtable", len(vTable)      
        print "x vertex", geoTable
        
        
        vertex(geoTable[vTable[c]].x, geoTable[vTable[c]].y, geoTable[vTable[c]].z)
        vertex(geoTable[vTable[c+1]].x, geoTable[vTable[c+1]].y, geoTable[vTable[c+1]].z)
        vertex(geoTable[vTable[c+2]].x, geoTable[vTable[c+2]].y, geoTable[vTable[c+2]].z)
        

        endShape(CLOSE)

        if colFlag:
            fill(random(255), random(255), random(255))
        else:
            fill(255, 255, 255)
        #popMatrix()
        endShape(CLOSE)
    #popMatrix()

    if currCVisible:  #weighted sum of the 3 vertices of the current triangle a
        pushMatrix()
        currentVertex = geoTable[vTable[currC]]
        translate(currentVertex[0], currentVertex[1], currentVertex[2])
        sphere(0.1)
        popMatrix()
    


# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global vTable, geoTable, opTable
    vTable = []
    geoTable = []
    opTable = {}
    
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
    # vTable = []
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
    draw()
    print_mesh()

#Compute opposite table
def computeOTable(geoTable, vTable):
    global opTable


    #bucket sort
    # compile list of triplets for each corner c
    triplets = []
    
    for c in range(len(vTable)):
        triplets.append([min(vTable[nextCorner(c)], vTable[prevCorner(c)]), max(vTable[nextCorner(c)], vTable[prevCorner(c)]), c])
    print "next corner", min(nextCorner(0), prevCorner(0)), max(nextCorner(1), prevCorner(1)), c
    sorted_triplets = sorted(triplets)
    #[([0, 2, 3], 0), ([1, 2, 2], 1), ([0, 2, 3], 2), ([1, 3, 1], 3), ([2, 3, 0], 4), ([1, 2, 2], 5), ([0, 2, 3], 6), ([1, 2, 2], 7), ([2, 3, 0], 8), ([2, 3, 0], 9), ([1, 3, 1], 10), ([0, 2, 3], 11)]
    # print "triplets", triplets
    # print(sorted_triplets)

    for i in range(0, len(sorted_triplets), 2):     
        cornerA = sorted_triplets[i][2]             
        cornerB = sorted_triplets[i+1][2]
        opTable[cornerA] = cornerB
        opTable[cornerB] = cornerA
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
        draw()
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
        
        #update global variables by calling subdivide 
        global vTable, geoTable, opTable
        vTable, geoTable, opTable = subdivideMesh(vTable, geoTable, opTable)
        print_mesh()
        #print "optable", opTable
        #print "vTable", vTable
        draw()
    elif key == 'i': # inflate mesh
        inflateMesh()
        
    elif key == 'r': # toggle random colors
        global colFlag
        colFlag = True
        pass
    elif key == 'c': # toggle showing current corner
        global currCVisible
        currCVisible = True
        
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
    #nCorner = (3 * triNum + (cornerNum+1) % 3)
    return (3 * triNum + (cornerNum+1) % 3)

def prevCorner(cornerNum):
    triNum = cornerNum // 3
    #pCorner = 
    return (3 * triNum + (cornerNum-1) % 3)

def oppositeCorner(cornerNum):
    # Use the opposite-table dictionary
    # Return O[cornerNum]
    return opTable[cornerNum]

#subdivision. Need copy old vertices (gtable)(do a slice), then append afterward. 
def subdivideMesh(vTable, geoTable, opTable):
    newOTable = opTable
    midpoints = {}
    newGeoTable = geoTable[:]
    #newVTable = vTable[:]
    newVTable = []
    #numTris = len(vTable) // 3

    
    for a, b in newOTable.iteritems():
        if a < b:
            endPoint1 = (geoTable[vTable[prevCorner(a)]])
            endPoint2 = (geoTable[vTable[nextCorner(a)]])
            endPoint1 = PVector(endPoint1[0], endPoint1[1], endPoint1[2])
            endPoint2 = PVector(endPoint2[0], endPoint2[1], endPoint2[2])
            type(endPoint2)
            midpoint = PVector.mult(PVector.add(endPoint1, endPoint2), 0.5)
            midpointIndex = len(newGeoTable)
            newGeoTable.append(midpoint)
            midpoints[a] = midpointIndex
            midpoints[b] = midpointIndex
            #print "midpoint", midpoint
            #print "endpoints", endPoint1, endPoint2 
            #Drawing Current corner. Weighted sum of corner.next, corner.prev, and corner 
            #offet = (constant * corner vertex + midpoint) / another constant
    k = 0
    for x in range(0, len(vTable), 3):
        y = x+1
        z = x+2
        #use the new vertices to match with a corner in the vertex table
        newVTable.extend([vTable[x], midpoints[z], midpoints[y],
                        midpoints[z], vTable[y], midpoints[x],
                        midpoints[y], midpoints[x], vTable[z],
                        midpoints[x], midpoints[y], midpoints[z]])
      
    print(len(newVTable))
    #print "newVTable", newVTable
    newOTable = computeOTable(newGeoTable, newVTable)
    return newVTable, newGeoTable, newOTable #or return computeOTable()

def inflateMesh(geoTable):
    #normalize
    geoTable = norm_vertices(geoTable)


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

def norm_vertices(vertices):
    for v in vertices:
        len = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        v[0] = v[0]/len * 1
        v[1] = v[1]/len * 1
        v[2] = v[2]/len * 1
    return vertices

class my_dictionary(dict):
 
  # __init__ function
  def __init__(self):
    self = dict()
 
  # Function to add key:value
  def add(self, key, value):
    self[key] = value

# 