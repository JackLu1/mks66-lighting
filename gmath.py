import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

# INDICES
AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
# COnstant not index
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize( view )
    normalize( normal )
    normalize( light[0] )
    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)
    color = limit_color([ambient[i] + diffuse[i] + specular[i] for i in range(3)])
    return color

def calculate_ambient(alight, areflect):
    return [alight[i] * areflect[i] for i in range(3)]

def calculate_diffuse(light, dreflect, normal):
    return [light[1][i] * dreflect[i] * dot_product(normal, light[0]) for i in range(3)]

def calculate_specular(light, sreflect, view, normal):
    dp_rhvh = dot_product(normal, light[0])
    if dp_rhvh < 0:
        return [0,0,0]
    power = [ 2 * dp_rhvh * normal[i] - light[0][i] for i in range(3) ]
    power_final = dot_product( power, view ) ** SPECULAR_EXP
    return [light[1][i] * sreflect[i] * power_final for i in range(3)]

def limit_color(color):
    for k in range(3):
        if color[k] < 0:
            color[k] = 0
        elif color[k] > 255:
            color[k] = 255
    return [int(i) for i in color]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
