#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
from dateutil.tz import tzlocal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from visual import *
from vis import *


class Grafica():
    def __init__(self):
        # Variables
        self.length_first_arm = 70
        self.length_second_arm = 45
        self.radius_sphere = 12
        self.radius_second_sphere = 8
        self.h_floor = 1
        self.h_holder = 20
        self.h_base = 8
        self.h_sphere = 17
        self.h_first_arm = 17
        self.h_second_arm = self.h_first_arm + self.length_first_arm
        self.top = vector(0,0,self.h_first_arm)

    def create_scene(self, lista):
        self.lista = lista
        #scene
        self.scene = display(title='Brazo robotico',
             x=0, y=0, width=700, height=700,
             center=(0,0,0))
        # piso
        self.floor = box(pos=(0,0,0), size=(500,500,self.h_floor), color=color.blue)
        #soporte robot
        self.holder = box(pos=(0,0,1),size=(50,50,self.h_holder),color=color.red)
        #base del robot (1er DOF)
        self.base = box(pos=(0,0,13),size=(25,25,self.h_base),color=color.green)
        self.frame3 = frame(pos=self.top)

        self.base_sphere = sphere(
          pos = (0,0,self.h_sphere),
          radius=self.radius_sphere)

        self.cylinder_first_brazo = cylinder(
          frame = self.frame3,
          pos=(0,0,0),
          length = self.length_first_arm,
          radius=5)

        self.union_sphere = sphere(
          frame = self.frame3,
          pos = (self.length_first_arm,0,0),
          radius=self.radius_second_sphere)

        self.frame3.axis=(0,0,1)
        self.frame4 = frame(pos = self.frame3.axis*self.h_first_arm)
        self.cylinder_first_arm = cylinder(
          frame = self.frame4,
          pos = (0,0,0),
          length = self.length_second_arm,
          radius=5)

        if (lista[0] == 0):
            self.run_directa(lista)
        else:
            self.run_inversa(lista)

    def run_directa(self,lista):
        dt = 0.00005
        self.frame3.rotate(axis=(0,1,0), angle=radians(float(self.lista[1])))
        self.frame3.rotate(axis=(0,0,1), angle=radians(float(self.lista[0])))
        self.frame4.pos = self.top+self.frame3.axis*self.length_first_arm
        self.frame4.axis = self.frame3.axis
        self.frame4.rotate(axis=(1,0,0), angle=radians(float(self.lista[2])))
        while True:
            rate(1/0.05)

    def run_inversa(self, lista):
        dt = 0.00005
        X = lista[1]
        Y = lista[2]
        Z = lista[3]
        #Angulo de la base hacia el punto
        angBase_Giro = math.atan2(float(Y),float(X))
        print "angBase_Giro: ",angBase_Giro
        #hallar el cateto de base hacia el punto
        Hipo  = math.sqrt((float(X)**2)+(float(Y)**2))
        print "hipotenusa: ", Hipo
        Xprima = Hipo
        #Igualamos la altura a Yprima
        Zprima = float(Z)+self.h_first_arm
        #Zprima = float(Z)
        hipotenusa = math.sqrt((Xprima**2)+(Zprima**2))
        alfa = math.atan2(float(Zprima),float(Xprima))
        a = float(self.length_first_arm**2+hipotenusa**2-self.length_second_arm**2)
        b = float(2*self.length_first_arm*hipotenusa)
        c = ((float(a/b))%2)-1
        beta = math.acos(c)
        a = float(self.length_second_arm**2+self.length_first_arm**2-hipotenusa**2)
        b = float(2*self.length_first_arm*self.length_second_arm)
        c = ((float(a/b))%2)-1
        gamma  = math.acos(c)
        # Angulos finales
        angBrazo = ((alfa + beta) - radians(180))
        angBase_Giro = (angBase_Giro)
        angAnBra = -(radians(180)-gamma)
        self.frame3.rotate(axis=(0,1,0), angle=angBrazo)
        self.frame3.rotate(axis=(0,0,1), angle=angBase_Giro)
        self.frame4.pos = self.top+self.frame3.axis*self.length_first_arm
        self.frame4.axis = self.frame3.axis
        self.frame4.rotate(axis = (1,0,0), angle=angAnBra)
        #print "Pos : ", self.frame4.pos + self.length_second_arm*vector(1,0,0)
        print "Pos : ", self.frame4.pos + self.length_second_arm*self.frame4.axis
        print "ang base de giro: ", angBase_Giro
        print "alfa: ",angBrazo
        print "gamma: ",angAnBra
        while True:
            rate(1/0.05)

class ventanaEvento(QDialog):
    def __init__(self, grafico,parent=None):
        #QDialog.__init__(self, parent)
        super(ventanaEvento, self).__init__(parent)
        #nombre, importancia, alerta, descripcion, fecha_inicio, fecha_fin
        self.grafico = grafico

        TituloDirecta = QLabel('CINEMATICA DIRECTA')
        TituloInversa = QLabel('CINEMATICA INVERSA')

        self.aceptarBoton = QPushButton("Cinematica Directa", self)
        self.cancelarBoton = QPushButton("Cancelar")

        self.aceptarBotonInversa = QPushButton("Cinematica Inversa", self)

        first_angle = QLabel('Primer angulo z')
        second_angle = QLabel('Segundo angulo y')
        third_angle = QLabel('Tercer angulo x')

        pos_x = QLabel('Posicion X')
        pos_y = QLabel('Posicion Y')
        pos_z = QLabel('Posicion Z')

        self.editFirst = QLineEdit()
        self.editSecond = QLineEdit()
        self.editThird = QLineEdit()

        self.editPosX = QLineEdit()
        self.editPosY = QLineEdit()
        self.editPosZ = QLineEdit()

        grid = QGridLayout()
        grid.addWidget(TituloDirecta,0,1)
        grid.addWidget(first_angle,1,0)
        grid.addWidget(self.editFirst,1,1)
        grid.addWidget(second_angle,2,0)
        grid.addWidget(self.editSecond,2,1)
        grid.addWidget(third_angle,3,0)
        grid.addWidget(self.editThird,3,1)
        grid.addWidget(self.aceptarBoton,4,1)

        grid.addWidget(TituloInversa,0,4)
        grid.addWidget(pos_x,1,3)
        grid.addWidget(self.editPosX,1,4)
        grid.addWidget(pos_y,2,3)
        grid.addWidget(self.editPosY,2,4)
        grid.addWidget(pos_z,3,3)
        grid.addWidget(self.editPosZ,3,4)
        grid.addWidget(self.aceptarBotonInversa,4,4)

        self.setLayout(grid)

        size=self.size()
        desktopSize=QDesktopWidget().screenGeometry()
        top=(desktopSize.height()/2)-(size.height()/2)
        left=(desktopSize.width()/2)-(size.width()/2)
        self.move(left, top)
        self.setWindowTitle('Cinematica directa e inversa')
        self.show()

        self.cancelarBoton.clicked.connect(self.close)
        self.connect(self.aceptarBoton, SIGNAL("clicked()"), self.Crear)
        self.connect(self.aceptarBotonInversa, SIGNAL("clicked()"), self.CrearInversa)

    def Crear(self):
        first_angle = unicode(self.editFirst.text())
        second_angle = unicode(self.editSecond.text())
        third_angle = unicode(self.editThird.text())
        lista = []
        lista.append(0)
        lista.append(first_angle)
        lista.append(second_angle)
        lista.append(third_angle)
        self.grafico.create_scene(lista)

    def CrearInversa(self):
        pos_x = unicode(self.editPosX.text())
        pos_y = unicode(self.editPosY.text())
        pos_z = unicode(self.editPosZ.text())
        lista = []
        lista.append(1)
        lista.append(pos_x)
        lista.append(pos_y)
        lista.append(pos_z)
        self.grafico.create_scene(lista)

def main():
    app = QApplication(sys.argv)
    grafico = Grafica()
    princial = ventanaEvento(grafico)
    princial.showMaximized()
    sys.exit(app.exec_())

main()