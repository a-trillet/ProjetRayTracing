import cmath
from Wall import *
from main import xMAP, yMAP, nbReflexion
from Ray import *
import Wall
"""objet Rayon, et une fonction qui calcule les coefficien de transmission"""


class DiffRay(Ray):
    def __init__(self, originX, originY, receiverX, receiverY, cornerx, cornery):
        super().__init__(originX, originY, receiverX, receiverY)

        self.Ppoints = [[cornerx, cornery]]

    def isacceptable(self, wallsh, wallsv):    #not accepted if ray is blocked by a wall or pass through a corner or if there is 3 points at edge
        if self.checkBlockingWall(wallsh, wallsv)[0]:
            return False
        else:
            corner = []
            wallsCorner = []
            for wH in wallsh:
                if wH.origin == self.Ppoints[0]:
                    corner.append(1)   # 1 to indicate that it is the low corner of the wall
                    wallsCorner.append(wH.origin[1])
                elif [wH.origin[0] + wH.xDirection, wH.origin[1]] == self.Ppoints[0]:
                    corner.append(0)
                    wallsCorner.append(wH.origin[1])
            for wV in wallsv:
                if wV.origin == self.Ppoints[0]:
                    corner.append(1)   # 1 to indicate that it is the low corner of the wall
                    wallsCorner.append(wV.origin[0])
                elif [wV.origin[0], wV.origin[1] + wV.yDirection] == self.Ppoints[0]:
                    corner.append(0)
                    wallsCorner.append(wV.origin[0])
            if len(corner) == 1:
                return True
            elif len(corner) == 2:
                if corner == [0, 0]:
                    if (self.originY <= wallsCorner[0] and self.originX <= wallsCorner[1]) or (self.receiverY <= wallsCorner[0] and self.receiverX <= wallsCorner[1]):
                        return False
                elif corner == [0, 1]:
                    if (self.originY >= wallsCorner[0] and self.originX <= wallsCorner[1]) or (self.receiverY >= wallsCorner[0] and self.receiverX <= wallsCorner[1]):
                        return False
                elif corner == [1, 1]:
                    if (self.originY >= wallsCorner[0] and self.originX >= wallsCorner[1]) or (self.receiverY >= wallsCorner[0] and self.receiverX >= wallsCorner[1]):
                        return False
                elif corner == [1, 0]:
                    if (self.originY <= wallsCorner[0] and self.originX >= wallsCorner[1]) or (self.receiverY <= wallsCorner[0] and self.receiverX >= wallsCorner[1]):
                        return False
                return True
            else:
                return False

    def diffractionCoef(self, beta):
        dLOS = math.sqrt((self.receiverX - self.originX)**2 + (self.receiverY - self.originY)**2)
        dDIFRA = math.sqrt((self.receiverX - self.Ppoints[0][0])**2 + (self.receiverY - self.Ppoints[0][1])**2) + math.sqrt((self.Ppoints[0][0] - self.originX)**2 + (self.Ppoints[0][1] - self.originY)**2)
        deltaR = dDIFRA-dLOS
        v = math.sqrt(2 / math.pi * beta * deltaR)
        modF = -3.45 - 10*math.log10(math.sqrt((v-0.1)**2 + 1) + v - 0.1)
        modF = 10**(modF / 10)
        argF = -math.pi*(1/4+(v**2)/2)
        F = modF * cmath.exp(complex(0, argF))
        return F

