import cmath
import math

from Wall import *
from main import xMAP, yMAP, nbReflexion
"""objet Rayon, et une fonction qui calcule les coefficien de transmission"""


class Ray:
    def __init__(self, originX, originY, receiverX, receiverY):
        self.originX = originX
        self.originY = originY
        self.receiverX = receiverX
        self.receiverY = receiverY
        self.imagePoints = []
        self.walls = []
        self.cosOiV = 0
        self.sinOiV = 0

        self.Ppoints = []

    def getLength(self):
        length = 0
        if len(self.imagePoints) == 0:
            if len(self.Ppoints) == 0:
                length = math.sqrt((self.receiverX - self.originX) ** 2 + (self.receiverY - self.originY) ** 2)
            else:
                length = math.sqrt((self.Ppoints[0][0] - self.originX) ** 2 + (self.Ppoints[0][1] - self.originY) ** 2)
                length += math.sqrt((self.Ppoints[0][0] - self.receiverX) ** 2 + (self.Ppoints[0][1] - self.receiverY) ** 2)
        else:
            length = math.sqrt((self.imagePoints[-1][0] - self.receiverX) ** 2 + (self.imagePoints[-1][1] - self.receiverY) ** 2)
        return length

    def getTcoef(self, wallsH, wallsV):  #transmition
        """ transmission coef squared for each wall transmitted through"""
        facEpsbrick = 0.4662524041201569
        facEpsconcrete = 0.4472135954999579
        Tcoef_carre = 1
        alphaMconcrete = 1.1793519138628281
        alphaMbrick = 1.756512304000713
        beta = 565.878155926954
        betaMconcrete = 1265.3425732375354
        betaMbrick = 1213.674704016611
        Z1 = 376.73031346177066
        Z2concrete = (168.47869848039613 + 0.15702915534584408j)
        Z2brick = (175.6508624825743 + 0.2542138351688341j)
        for i in range(len(self.Ppoints) + 1):
            if i == 0 and len(self.Ppoints) != 0:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.Ppoints[0][0]
                Py2 = self.Ppoints[0][1]
            elif len(self.Ppoints) == 0:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.receiverX
                Py2 = self.receiverY
            elif i == len(self.Ppoints):
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.receiverX
                Py2 = self.receiverY
            else:
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.Ppoints[i][0]
                Py2 = self.Ppoints[i][1]
            dx = Px2 - Px1
            dy = Py2 - Py1
            d = math.sqrt(dx ** 2 + dy ** 2)
            # Walls H
            TmB = 0
            TmC = 0
            cosOi = -dy / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dx / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            for wall in wallsH:  # n= (0,-1)
                if Py1 < wall.origin[1] < Py2 or Py1 > wall.origin[1] > Py2:
                    proj = (wall.origin[1] - Py2) * sinOi / cosOi
                    if wall.origin[0] < Px2 - proj < wall.origin[0] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                cosOtC = math.sqrt(1 - sinOi ** 2 / 5)
                                gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOtC) / (Z2concrete * abs(cosOi) + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,
                                                      (
                                                          facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1 - gammaPerp ** 2) * math.exp(-alphaMconcrete/2/cosOtC) / (
                                            1 - gammaPerp ** 2 * u))
                            Tcoef_carre *= TmC ** 2
                        elif wall.mat == 0:
                            if TmB == 0:
                                cosOtB = math.sqrt(1 - sinOi ** 2 / 4.6)
                                gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOtB) / (Z2brick * abs(cosOi) + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                      (
                                                          facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1 - gammaPerp ** 2) * math.exp(-alphaMbrick/2/cosOtB) / (
                                            1 - gammaPerp ** 2 * u))
                            Tcoef_carre *= TmB ** 2
                elif wall.origin[1] > Py1 and wall.origin[1] > Py2:
                    break
            # Walls V
            TmB = 0
            TmC = 0
            cosOi = dx / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dy / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            for wall in wallsV:  # n= (1,0)
                if Px1 < wall.origin[0] < Px2 or Px1 > wall.origin[0] > Px2:
                    proj = (Px2 - wall.origin[0]) * sinOi / cosOi
                    if wall.origin[1] <= Py2 - proj <= wall.origin[1] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                cosOtC = math.sqrt(1 - sinOi ** 2 / 5)
                                gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOtC) / (Z2concrete * abs(cosOi) + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,(facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1 - gammaPerp ** 2) * math.exp(-alphaMconcrete/2/cosOtC) / (1 - gammaPerp ** 2 * u))
                            Tcoef_carre *= TmC ** 2
                        elif wall.mat == 0:
                            if TmB == 0:
                                cosOtB = math.sqrt(1 - sinOi ** 2 / 4.6)
                                gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOtB) / (Z2brick * abs(cosOi) + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                      (
                                                          facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1 - gammaPerp ** 2) * math.exp(-alphaMbrick/2/cosOtB) / (
                                        1 - gammaPerp ** 2 * u))
                            Tcoef_carre *= TmB ** 2
                elif wall.origin[0] > Px1 and wall.origin[0] > Px2:
                    break
        # print(Tcoef_carre)
        return Tcoef_carre  # NOTE: carré ou pas à voir

    def checkBlockingWall(self, wallsH, wallsV):
        if len(self.Ppoints) == 0:
            DirectWave = True
        else:
            DirectWave = False
        blockingWalls = []
        blocking = False
        for i in range(len(self.Ppoints) + 1):
            if i == 0 and not DirectWave:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.Ppoints[0][0]
                Py2 = self.Ppoints[0][1]
            elif DirectWave:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.receiverX
                Py2 = self.receiverY
            elif i == len(self.Ppoints):
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.receiverX
                Py2 = self.receiverY
            else:
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.Ppoints[i][0]
                Py2 = self.Ppoints[i][1]
            dx = Px2 - Px1
            dy = Py2 - Py1
            d = math.sqrt(dx ** 2 + dy ** 2)
            # Walls H
            cosOi = -dy / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dx / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            for wall in wallsH:  # n= (0,-1)
                if Py1 < wall.origin[1] < Py2 or Py1 > wall.origin[1] > Py2:
                    proj = (wall.origin[1] - Py2) * sinOi / cosOi
                    if wall.origin[0] < Px2 - proj < wall.origin[0] + wall.length:
                        blocking = True
                        if not DirectWave:
                            break
                        blockingWalls.append(wall)

                elif wall.origin[1] > Py1 and wall.origin[1] > Py2:  #walls are sorted so that we don't need to go through all of them
                    break
            # Walls V
            cosOi = dx / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dy / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            for wall in wallsV:  # n= (1,0)
                if Px1 < wall.origin[0] < Px2 or Px1 > wall.origin[0] > Px2:
                    proj = (Px2 - wall.origin[0]) * sinOi / cosOi
                    if wall.origin[1] <= Py2 - proj <= wall.origin[1] + wall.length:
                        blocking = True
                        if not DirectWave:
                            break
                        blockingWalls.append(wall)

                elif wall.origin[0] > Px1 and wall.origin[0] > Px2:
                    break

        return blocking, blockingWalls         #true or false and blocking walls if ray is LOS

    def getGroundReflexion(self, lam):    # Note: (he is  // En) (not applicable if ray reflected on walls before/after)
        if len(self.Ppoints) != 0:
            print("Can't compute the ground reflexion for a ray that reflected on walls")
            return 0
        height = 2
        dXY2 = (self.receiverX-self.originX)**2 + (self.receiverY-self.originY)**2
        d = math.sqrt((2*height)**2 + dXY2)
        Og = math.atan(d/(2*height))    # angle with the ground
        Oi = math.pi - Og               # angle with the antennas
        permRel = 4   # relative permittivity of the ground is set to 4.5 as for the buildings
        Gtx = 1.7 * math.sin(Oi) ** 3
        Ptx = 0.1471

        he = -lam / math.pi * math.cos(math.pi/2 * math.cos(Oi)) / math.sin(Oi)**2

        temp = math.sqrt(1 - (math.sin(Og)**2)/permRel) / math.sqrt(permRel)
        GammaPar = (math.cos(Og) - temp) / (math.cos(Og) + temp)

        beta = 2 * math.pi / lam
        Voc = GammaPar * he * math.sqrt(60 * Gtx * Ptx) * cmath.exp(complex(0, -beta * d)) / d
        return Voc, d
