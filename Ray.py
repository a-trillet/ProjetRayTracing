import cmath

import inline as inline
import pylab

from Wall import *
import numpy as np
import pylab
import inline


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

    def getTcoef(self, wallsH, wallsV):
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
        return Tcoef_carre  # NOTE: carré ou pas à voir
