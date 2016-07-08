# ver resident evil Damnation

from visual import *
from vis import *
import wx
import sys
import os
import math
# Variables

length_first_arm = 70
length_second_arm = 45
radius_sphere = 12
radius_second_sphere = 8
h_floor = 1
h_holder = 20
h_base = 8
h_sphere = 17
h_first_arm = 17
h_second_arm = h_first_arm + length_first_arm
top = vector(0,0,h_first_arm)

#scene
scene = display(title='Brazo robotico',
     x=0, y=0, width=600, height=800,
     center=(0,0,0))

# piso
floor = box(pos=(0,0,0), size=(500,500,h_floor), color=color.blue)

#soporte robot
holder = box(pos=(0,0,1),size=(50,50,h_holder),color=color.red)

#base del robot (1er DOF)
base = box(pos=(0,0,13),size=(25,25,h_base),color=color.green)

frame3 = frame(pos=top)

dt = 0

base_sphere = sphere(
  pos = (0,0,h_sphere),
  radius=radius_sphere)

cylinder_first_brazo = cylinder(
  frame = frame3,
  pos=(0,0,0),
  length = length_first_arm,
  radius=5)

union_sphere = sphere(
  frame = frame3,
  pos = (length_first_arm,0,0),
  radius=radius_second_sphere)

frame3.axis=(0,0,1)
frame4 = frame(pos = frame3.axis*h_first_arm)

cylinder_first_arm = cylinder(
  frame = frame4,
  pos = (0,0,0),
  length = length_second_arm,
  radius=5)

def rotar_x(a,b,c):
    frame3.rotate(axis=(0,0,1), angle=radians(a))
    frame4.pos = top + frame3.axis * length_first_arm
    print "Pos : ", frame4.pos + length_second_arm*frame4.axis

def rotar_y(a,b,c):
    frame3.rotate(axis=(0,1,0), angle=radians(b))
    frame4.pos = top + frame3.axis * length_first_arm
    print "Pos : ", frame4.pos + length_second_arm*frame4.axis

def rotar_z(a,b,c):
    frame4.pos = top + frame3.axis * length_first_arm
    frame4.axis = frame3.axis
    frame4.rotate(axis = (1,0,0), angle=radians(c))
    #frame4.rotate(angle=radians(c))
    print frame4.axis
    print "Pos : ", frame4.pos + length_second_arm*frame4.axis

x = 0
y = 0
z = 0

def run_directa(evento):
    global x
    global y
    global z
    val = evento.key
    if(val == 'x'):
      x = (x + 0.1)%360
      y = 0
      z = 0
      rotar_x(x,y,z)
    elif(val == 'y'):
      y = (y + 0.1)%360
      x = 0
      z = 0
      rotar_y(x,y,z)
    elif(val == 'z'):
      z = (z + 1)%360
      y = 0
      x = 0
      rotar_z(x,y,z)
    print "Angulo base giro: ",radians(x)
    print "Angulo base caida: ",radians(y)
    print "Angulo Antebrazo: ",radians(z)
    
def run_inversa(evento):
    global x
    global y
    global z
    val = evento.key
    if(val == 'x'):
      x +=1 
    elif(val == 'y'):
      y +=1
    elif(val == 'z'):
      z += 1 
    print x, y, z
    dt = 0.00005
    #Angulo de la base hacia el punto
    angBase_Giro = math.atan2(float(y),float(x))
    print "ang base de giro: ", angBase_Giro
    #hallar el cateto de base hacia el punto
    Hipo  = math.sqrt((float(x)**2)+(float(y)**2))
    Xprima = Hipo
    #Igualamos la altura a Yprima
    Zprima = float(z)+h_first_arm
    print "Xprima:", Xprima, " Z:", Zprima

    hipotenusa = math.sqrt((Xprima**2)+(Zprima**2))
    print "hipotenusa: ", hipotenusa
    alfa = math.atan2(float(Zprima),float(Xprima))
    a = float(length_second_arm**2-length_first_arm**2-hipotenusa**2)
    b = float(-2*length_first_arm*hipotenusa)
    c = ((float(a/b))%2)-1
    print "c: ",c
    print "alfa: ",alfa
    print a,b
    beta = math.acos(c)
    a = float(hipotenusa**2-length_second_arm**2-length_first_arm**2)
    b = float(-2*length_first_arm*length_second_arm)
    c = ((float(a/b))%2)-1
    gamma  = math.acos(c)
    print "gamma: ",gamma
    # Angulos finales
    angBrazo = -((alfa + beta)-radians(180))
    angAnBra = -(gamma - radians(180))
    frame3.rotate(axis=(0,1,0), angle=angBrazo)
    frame3.rotate(axis=(0,0,1), angle=angBase_Giro)
    frame4.pos = top+frame3.axis*length_first_arm
    frame4.axis = frame3.axis
    frame4.rotate(axis=(1,0,0), angle=angAnBra)
    while True:
        rate(1/0.05)

scene.bind('keydown', run_directa)
#scene.bind('keydown', run_inversa)