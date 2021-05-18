import math
"""Objet mur"""


mu0 = 4 * math.pi * 10 ** (-7)
class Wall:
    def __init__(self, xOrigin, yOrigin, xDirection, yDirection, material):
        self.length = math.sqrt(xDirection ** 2 + yDirection ** 2)
        self.uX = int(xDirection/self.length)                    #vecteur U // au mur
        self.uY = int(yDirection/self.length)
        self.nX = int(yDirection/self.length)                        #vecteur N normal au mur
        self.nY = int(-xDirection/self.length)
        self.origin = [xOrigin, yOrigin]

        self.mat = -1
        self.relativePermitivity = 0
        self.condctivity = 0
        self.thickness = 0.5                                #en mètre
        self.xDirection = int(xDirection)                        #pour l'affichage
        self.yDirection = int(yDirection)

        self.setProperty(material)


    def getOriginX(self):
        return self.origin[0]

    def getOriginY(self):
        return self.origin[1]

    def getNx(self):
        return self.nX

    def getNy(self):
        return self.nY

    def setProperty(self, material):
        if material == "brick":
            self.mat = 0
            self.condctivity = 0.02
            self.relativePermitivity = 4.6
        elif material == "concrete":
            self.mat = 1
            self.condctivity = 0.014
            self.relativePermitivity = 5
        elif material == "partition":
            self.mat = 2
            self.condctivity = 0.04
            self.relativePermitivity = 2.25
        else:
            print("matériau inconnu")

